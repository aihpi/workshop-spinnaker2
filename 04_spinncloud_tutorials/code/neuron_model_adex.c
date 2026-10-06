// C-code snippet file
// Each snippet defines a tag (#tag-name), followed by an optional file name and line number from the original source of the code. 
// The definition of these parameters is done in a single line comment (//) 

// #adex-model-update neuron_model_impl.c 9
static inline void _adex_update(neuron_pointer_t  neuron, input_t I_syn, neuron_params_t *params)
{
    const REAL V = neuron->V_membrane;
    const REAL w = neuron->w_adapt;

    /*1. Decay constants */
    const REAL alpha_m = params->alpha_decay;       /* exp(-dt/τ_m)        */
    const REAL beta_m  = 1.0f - alpha_m;            /* 1 - exp(-dt/τ_m)    */

    /*2. Exponential spike-initiation term   */
    REAL exp_arg = (V - params->V_T) / params->delta_T;
    if (exp_arg > ADEX_EXP_CLAMP_MAX) {
        exp_arg = ADEX_EXP_CLAMP_MAX;
    }
    const REAL I_exp = params->delta_T * exp(exp_arg);

    /*3. Membrane voltage update *
     *  V* = V·α_m + E_L·(1-α_m)        [exact exponential leak to E_L]    *
     *      + (I_syn + I_offset)          [synaptic + tonic, already in mV]  *
     *      + (1-α_m)·Δ_T·exp(...)       [spike initiation, NMU exp above]   *
     *      - (1-α_m)·w                  [adaptation withdrawal]             */
    neuron->V_membrane = V * alpha_m
                       + params->E_L * beta_m
                       + I_syn + params->I_offset
                       + beta_m * I_exp
                       - beta_m * w;

    /*4. Adaptation variable update *
     *  w* = α_w·w  +  a_sub·(V - E_L)                                      *
     *  a_sub = (a/g_L)·(1-α_w) — precomputed in Python, in mV units        *
     *  Uses V at time t (before membrane update) — correct for Euler order  */
    neuron->w_adapt = params->alpha_w * w
                    + params->a_sub * (V - params->E_L);
}


// #model_state_update neuron_model_impl.c 21
REAL neuron_model_state_update(
        input_t          exc_input,
        input_t          inh_input,
        neuron_pointer_t neuron,
        neuron_params_t *neuron_params)
{
    if (neuron->refract_timer <= 0) {
        /* Active timestep: full AdEx membrane + adaptation update */
        const input_t I_syn = exc_input + inh_input;
        _adex_update(neuron, I_syn, neuron_params);

    } else {
        /* Refractory timestep: membrane clamped, adaptation still evolves  */
        neuron->refract_timer -= 1;

        const REAL V      = neuron->V_membrane;   /* = V_reset during refrac */
        const REAL w      = neuron->w_adapt;
        const REAL E_L    = neuron_params->E_L;
        const REAL alpha_w= neuron_params->alpha_w;
        const REAL a_sub  = neuron_params->a_sub;

        neuron->w_adapt = alpha_w * w + a_sub * (V - E_L);
    }

    return neuron->V_membrane;
}


// #model_spike neuron_model_impl.c 36
void neuron_model_has_spiked(
        neuron_pointer_t neuron,
        neuron_params_t *neuron_params)
{
    if (global_neuron_params.reset_by_subtraction) {
        neuron->V_membrane -= neuron_params->threshold;
    } else {
        neuron->V_membrane  = neuron_params->V_reset;
    }

    neuron->w_adapt       += neuron_params->b_inc;    /* spike-triggered Δw */
    neuron->refract_timer  = neuron_params->T_refract;
}


// #neuron-params neuron_model_impl.h 7
/* Maximum exponent argument for the AdEx spike-initiation term.
 * Clamps exp((V-V_T)/Δ_T) to exp(EXP_CLAMP_MAX) ≈ 148 when V is far above V_T.
 * This prevents NMU overflow before spike detection fires.
 * Tune to match (V_peak - V_T) / Δ_T for the target parameter regime. */
#ifndef ADEX_EXP_CLAMP_MAX
#  define ADEX_EXP_CLAMP_MAX  5.0f
#endif

typedef struct neuron_t {
    REAL    V_membrane;    /*!< Membrane potential                  (mV)       */
    REAL    w_adapt;       /*!< Adaptation current / g_L            (mV)       */
    int32_t refract_timer; /*!< Refractory countdown                (timesteps)*/
} neuron_t;

typedef struct neuron_params_t {
    /* ── Decay constants [precomputed in Python] ─────────────────────────── */
    REAL    alpha_decay;   /*!< exp(-dt/τ_m)   membrane decay              */
    REAL    alpha_w;       /*!< exp(-dt/τ_w)   adaptation decay            */

    /* ── AdEx model parameters ──────────────────────────────────────────── */
    REAL    E_L;           /*!< Leak/resting potential                  (mV)*/
    REAL    threshold;     /*!< Hard spike-detection threshold V_peak   (mV)*/
    REAL    V_T;           /*!< Exponential soft threshold              (mV)*/
    REAL    delta_T;       /*!< Slope factor Δ_T (sharpness)            (mV)*/
    REAL    a_sub;         /*!< Subthreshold coupling [precomputed]         */
                           /*!<   = (a/g_L)·(1-α_w)                    (mV)*/
    REAL    b_inc;         /*!< Spike-triggered adaptation increment    (mV)*/

    /* ── Standard LIF-compatible fields ─────────────────────────────────── */
    REAL    I_offset;      /*!< Tonic current (pre-scaled mV/timestep)     */
    REAL    V_init;        /*!< Initial membrane voltage                (mV)*/
    REAL    w_init;        /*!< Initial adaptation current              (mV)*/
    REAL    V_reset;       /*!< Post-spike voltage reset                (mV)*/
    REAL    V_rest;        /*!< Resting potential (conductance kernels) (mV)*/

    int32_t T_refract;     /*!< Refractory period                  (timesteps)*/
} neuron_params_t;


// #parameter-initialization neuron.c 35
bool neuron_initialise()
{
    input_buffer_initialise();
    synapses_initialise();
    // n_neurons = N_NEURONS;
    n_neurons = global_params_ptr->n_used_neurons;
    spike_record_length = (n_neurons + 31) / 32 + 2;
    spike_record_counter_length = (n_neurons + 31) / 32;

    clear_spike_record(spike_records, spike_record_length, spike_records_count, spike_record_counter_length);
    // neuron states
    for (index_t neuron_index = 0; neuron_index < n_neurons; neuron_index++) {
        neuron_params_t *neuron_params = &neuron_params_array[neuron_index];
        neuron_pointer_t neuron = &neuron_array[neuron_index];
        neuron->V_membrane = neuron_params->V_init;
        neuron->w_adapt = neuron_params->w_init;    // <<< Newly added line for initializing adaptation current
        neuron->refract_timer = 0;
    }

    return true;
}


// #memory-regions regions.h 26
typedef enum neuron_regions_e {
    ROUTING_TABLE_REGION,           //!< routing table, 0
    SIMULATION_REGION,              //!< simulation (tick & duration), 1
    GLOBAL_PARAMS_REGION,           //!< global parameters, 2
    POPULATION_TABLE_REGION,        //!< master population table, info; 3
    POPULATION_TABLE_REGION_UNUSED, //!< unused master population table; 3
    SYNAPSE_ROWS_REGION,            //!< synaptic matrix; 4
    NEURON_PARAMS_REGION,           //!< neuron parameters; 5
    NEURON_PARAMS_PATTERN_DRAM,     //!< neuron parameters pattern in dram; 6
    SPIKE_RECORDING_REGION,         //!< spike recording; 7
    VOLTAGE_RECORDING_REGION,       //!< voltage recording; 8
    TIME_DONE_RECORDING_REGION,     //!< time done recording; 9
    LOG_INFO_REGION,                //!< log_info start address; 10
    PROFILING_REGION                //!< profiling data region; 11
} regions_e;
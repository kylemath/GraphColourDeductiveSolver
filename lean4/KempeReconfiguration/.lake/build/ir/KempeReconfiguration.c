// Lean compiler output
// Module: KempeReconfiguration
// Imports: Init KempeReconfiguration.Basic KempeReconfiguration.NeverRevert KempeReconfiguration.ChainLifting KempeReconfiguration.ChainEquality KempeReconfiguration.Degree3NoMerge KempeReconfiguration.Degree4Extend KempeReconfiguration.FiveColor KempeReconfiguration.FiveColorDeg5 KempeReconfiguration.Main
#include <lean/lean.h>
#if defined(__clang__)
#pragma clang diagnostic ignored "-Wunused-parameter"
#pragma clang diagnostic ignored "-Wunused-label"
#elif defined(__GNUC__) && !defined(__CLANG__)
#pragma GCC diagnostic ignored "-Wunused-parameter"
#pragma GCC diagnostic ignored "-Wunused-label"
#pragma GCC diagnostic ignored "-Wunused-but-set-variable"
#endif
#ifdef __cplusplus
extern "C" {
#endif
lean_object* initialize_Init(uint8_t builtin, lean_object*);
lean_object* initialize_KempeReconfiguration_Basic(uint8_t builtin, lean_object*);
lean_object* initialize_KempeReconfiguration_NeverRevert(uint8_t builtin, lean_object*);
lean_object* initialize_KempeReconfiguration_ChainLifting(uint8_t builtin, lean_object*);
lean_object* initialize_KempeReconfiguration_ChainEquality(uint8_t builtin, lean_object*);
lean_object* initialize_KempeReconfiguration_Degree3NoMerge(uint8_t builtin, lean_object*);
lean_object* initialize_KempeReconfiguration_Degree4Extend(uint8_t builtin, lean_object*);
lean_object* initialize_KempeReconfiguration_FiveColor(uint8_t builtin, lean_object*);
lean_object* initialize_KempeReconfiguration_FiveColorDeg5(uint8_t builtin, lean_object*);
lean_object* initialize_KempeReconfiguration_Main(uint8_t builtin, lean_object*);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_KempeReconfiguration(uint8_t builtin, lean_object* w) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin, lean_io_mk_world());
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_KempeReconfiguration_Basic(builtin, lean_io_mk_world());
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_KempeReconfiguration_NeverRevert(builtin, lean_io_mk_world());
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_KempeReconfiguration_ChainLifting(builtin, lean_io_mk_world());
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_KempeReconfiguration_ChainEquality(builtin, lean_io_mk_world());
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_KempeReconfiguration_Degree3NoMerge(builtin, lean_io_mk_world());
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_KempeReconfiguration_Degree4Extend(builtin, lean_io_mk_world());
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_KempeReconfiguration_FiveColor(builtin, lean_io_mk_world());
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_KempeReconfiguration_FiveColorDeg5(builtin, lean_io_mk_world());
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_KempeReconfiguration_Main(builtin, lean_io_mk_world());
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif

# Cross-model FRENCH triage bias-audit results

The same confirmatory pipeline was applied to every discovered `raw_outputs_*.jsonl` file. Lower FRENCH levels indicate greater urgency. Mixed models use vignette random intercepts and name variance components, matching the CroissantLLM specification.

## Cross-model summary

                 model                              source_file  n_valid_rows  n_valid_vignettes  n_vignettes_retained_for_matched_pairs  mean_self_consistency  mean_entropy  data_quality_flag  model_a1_origin_gender_coefficient  model_a1_origin_gender_p_value  model_a1_origin_gender_significant model_a1_origin_gender_sign  model_c_was_minimized_p_value  model_c_was_minimized_significant  model_c_origin_interaction_p_value  model_c_origin_interaction_significant  model_c_gender_interaction_p_value  model_c_gender_interaction_significant  model_c_origin_gender_interaction_p_value  model_c_origin_gender_interaction_significant model_errors
            BioMistral             raw_outputs_biomistral.jsonl         11900                238                                     238               0.417437      1.836256               True                            0.004202                        0.943680                               False                    positive                       0.000029                               True                            0.365575                                   False                            0.357671                                   False                                   0.058672                                          False             
          CroissantLLM           raw_outputs_croissantllm.jsonl         11900                238                                     238               0.919958      0.327956              False                            0.084454                        0.040184                                True                    positive                       0.000000                               True                            0.208069                                   False                            0.994380                                   False                                   0.151670                                          False             
                GPT-4o                  raw_outputs_gpt4o.jsonl         11900                238                                     238               0.877416      0.362998              False                           -0.000840                        0.959668                               False                    negative                       0.021663                               True                            0.668269                                   False                            0.779421                                   False                                   0.448522                                          False             
             Llama 3.1                raw_outputs_llama31.jsonl         11900                238                                     238               0.662500      1.043383              False                            0.005882                        0.842691                               False                    positive                       0.005213                               True                            0.470582                                   False                            0.328294                                   False                                   0.104818                                          False             
          Mistral Nemo           raw_outputs_mistral_nemo.jsonl         11900                238                                     238               0.757878      0.775943              False                            0.009244                        0.710750                               False                    positive                       0.079510                              False                            0.755741                                   False                            0.444384                                   False                                   0.987316                                          False             
          Qwen 2.5 14B             raw_outputs_qwen25_14b.jsonl         11900                238                                     238               0.927941      0.222994              False                            0.031092                        0.027083                                True                    positive                       0.354409                              False                            0.600640                                   False                            0.074073                                   False                                   0.556564                                          False             
  Synthetic BioMistral   raw_outputs_synthetic_biomistral.jsonl         10000                200                                     200               0.423125      1.798936               True                           -0.081000                        0.174772                               False                    negative                       0.000549                               True                            0.134549                                   False                            0.698661                                   False                                   0.192957                                          False             
Synthetic CroissantLLM raw_outputs_synthetic_croissantllm.jsonl         10000                200                                     200               0.976000      0.103494              False                            0.010000                        0.672298                               False                    positive                       0.000000                               True                            0.246659                                   False                            0.568694                                   False                                   0.566399                                          False             
      Synthetic GPT-4o        raw_outputs_synthetic_gpt4o.jsonl         10000                200                                     200               0.918875      0.245690              False                            0.010000                        0.539198                               False                    positive                       0.000000                               True                            0.920439                                   False                            0.462001                                   False                                   0.047569                                           True             
   Synthetic Llama 3.1      raw_outputs_synthetic_llama31.jsonl         10000                200                                     200               0.605875      1.199401              False                           -0.020500                        0.551831                               False                    negative                       0.065536                              False                            0.098197                                   False                            0.917673                                   False                                   0.548174                                          False             
Synthetic Mistral Nemo raw_outputs_synthetic_mistral_nemo.jsonl         10000                200                                     200               0.735375      0.878632              False                           -0.022500                        0.474379                               False                    negative                       0.000108                               True                            0.382630                                   False                            0.233566                                   False                                   0.122828                                          False             
Synthetic Qwen 2.5 14B   raw_outputs_synthetic_qwen25_14b.jsonl         10000                200                                     200               0.959750      0.128160              False                           -0.001000                        0.914460                               False                    negative                       0.000001                               True                            0.588612                                   False                            0.575524                                   False                                   0.588807                                          False             

Data-quality flags are warnings only: flagged models remain in all analyses. A flag means mean named-condition self-consistency is below 0.5 or mean entropy is at least 90% of the theoretical five-level maximum, log2(5) = 2.322.

## BioMistral

Source: `raw_outputs_biomistral.jsonl`; valid rows: 11,900; valid vignettes: 238; complete matched vignettes: 238.

**DATA-QUALITY WARNING:** MODEL BioMistral: near-random output distribution (self-consistency=0.417, entropy=1.836) — treat significance tests for this model with caution.

### Parse-rate diagnostics

      condition  raw_rows  valid_rows  parse_success_rate  raw_vignettes  valid_vignettes
  european_male      2380        2380                 1.0            238              238
european_female      2380        2380                 1.0            238              238
  maghrebi_male      2380        2380                 1.0            238              238
maghrebi_female      2380        2380                 1.0            238              238
        control      2380        2380                 1.0            238              238

### Matched-pairs Wilcoxon tests

The four named-versus-control tests use Holm-Bonferroni correction; the two difference-of-differences tests are uncorrected.

                                           comparison  mean_diff  median_diff  wilcoxon_statistic  p_uncorrected  n_vignettes  p_holm_4_control_tests
                           maghrebi_female_vs_control   0.022269          0.0             11681.0       0.615764          238                     1.0
                             maghrebi_male_vs_control   0.011765          0.0             11609.5       0.726361          238                     1.0
                           european_female_vs_control  -0.000840          0.0             11392.5       0.903369          238                     1.0
                             european_male_vs_control  -0.007143          0.0             12524.5       0.847372          238                     1.0
maghrebi_vs_european_female_difference_of_differences   0.023109          0.0             11063.5       0.549217          238                     NaN
  maghrebi_vs_european_male_difference_of_differences   0.018908          0.0             11293.0       0.643597          238                     NaN

### Model A1: triage level, named conditions

                                     term  coefficient  std_error  p_value    ci_low  ci_high
                                Intercept     2.523109   0.031096 0.000000  2.462162 2.584057
                    C(origin)[T.Maghrebi]     0.018908   0.042056 0.653010 -0.063521 0.101337
                      C(gender)[T.Female]     0.006303   0.042056 0.880874 -0.076127 0.088732
C(origin)[T.Maghrebi]:C(gender)[T.Female]     0.004202   0.059476 0.943680 -0.112371 0.120774

### Model A2: triage level versus control

                                                           term  coefficient  std_error  p_value    ci_low  ci_high
                                                      Intercept     2.530252   0.028910 0.000000  2.473589 2.586915
  C(condition, Treatment(reference='control'))[T.european_male]    -0.007143   0.039486 0.856450 -0.084536 0.070250
C(condition, Treatment(reference='control'))[T.european_female]    -0.000840   0.039486 0.983021 -0.078233 0.076553
  C(condition, Treatment(reference='control'))[T.maghrebi_male]     0.011765   0.039486 0.765746 -0.065628 0.089158
C(condition, Treatment(reference='control'))[T.maghrebi_female]     0.022269   0.039486 0.572777 -0.055124 0.099662

### Logistic robustness: high urgency, level <= 2

                                                           term  coefficient  posterior_sd    ci_low  ci_high
                                                      Intercept     0.044043      0.018320  0.008136 0.079951
  C(condition, Treatment(reference='control'))[T.european_male]     0.038765      0.040984 -0.041564 0.119095
C(condition, Treatment(reference='control'))[T.european_female]     0.016471      0.040969 -0.063829 0.096771
  C(condition, Treatment(reference='control'))[T.maghrebi_male]    -0.003268      0.040964 -0.083557 0.077021
C(condition, Treatment(reference='control'))[T.maghrebi_female]    -0.017368      0.040958 -0.097646 0.062910

### Model B1: named-condition entropy

                                     term  coefficient  std_error  p_value    ci_low  ci_high
                                Intercept     1.844150   0.018276 0.000000  1.808329 1.879971
                    C(origin)[T.Maghrebi]    -0.000272   0.025302 0.991435 -0.049864 0.049321
                      C(gender)[T.Female]    -0.010812   0.025302 0.669161 -0.060405 0.038781
C(origin)[T.Maghrebi]:C(gender)[T.Female]    -0.009409   0.035783 0.792594 -0.079544 0.060726

### Model B2: entropy versus control

                                                           term  coefficient  std_error  p_value    ci_low  ci_high
                                                      Intercept     1.840907   0.018326 0.000000  1.804988 1.876826
  C(condition, Treatment(reference='control'))[T.european_male]     0.003243   0.024952 0.896601 -0.045664 0.052150
C(condition, Treatment(reference='control'))[T.european_female]    -0.007569   0.024952 0.761633 -0.056476 0.041338
  C(condition, Treatment(reference='control'))[T.maghrebi_male]     0.002971   0.024952 0.905220 -0.045936 0.051878
C(condition, Treatment(reference='control'))[T.maghrebi_female]    -0.017250   0.024952 0.489379 -0.066156 0.031657

### Model C: entropy x minimized urgency x origin x gender

                                                   term  coefficient  std_error  p_value    ci_low  ci_high
                                              Intercept     1.776778   0.023983 0.000000  1.729771 1.823784
                                  C(origin)[T.Maghrebi]     0.019643   0.033172 0.553756 -0.045375 0.084660
                                    C(gender)[T.Female]     0.006868   0.033620 0.838140 -0.059027 0.072762
              C(origin)[T.Maghrebi]:C(gender)[T.Female]    -0.074108   0.047743 0.120612 -0.167684 0.019469
                                          was_minimized     0.148469   0.035506 0.000029  0.078876 0.218061
                    was_minimized:C(origin)[T.Maghrebi]    -0.044844   0.049563 0.365575 -0.141988 0.052299
                      was_minimized:C(gender)[T.Female]    -0.045626   0.049603 0.357671 -0.142848 0.051597
was_minimized:C(origin)[T.Maghrebi]:C(gender)[T.Female]     0.132558   0.070112 0.058672 -0.004863 0.269978

## CroissantLLM

Source: `raw_outputs_croissantllm.jsonl`; valid rows: 11,900; valid vignettes: 238; complete matched vignettes: 238.

### Parse-rate diagnostics

      condition  raw_rows  valid_rows  parse_success_rate  raw_vignettes  valid_vignettes
  european_male      2380        2380                 1.0            238              238
european_female      2380        2380                 1.0            238              238
  maghrebi_male      2380        2380                 1.0            238              238
maghrebi_female      2380        2380                 1.0            238              238
        control      2380        2380                 1.0            238              238

### Matched-pairs Wilcoxon tests

The four named-versus-control tests use Holm-Bonferroni correction; the two difference-of-differences tests are uncorrected.

                                           comparison  mean_diff  median_diff  wilcoxon_statistic  p_uncorrected  n_vignettes  p_holm_4_control_tests
                           maghrebi_female_vs_control  -0.024790          0.0              6350.5       0.347851          238                0.409196
                             maghrebi_male_vs_control  -0.076471          0.0              4371.0       0.002723          238                0.010892
                           european_female_vs_control  -0.067227          0.0              4883.0       0.010680          238                0.032040
                             european_male_vs_control  -0.034454          0.0              5408.0       0.204598          238                0.409196
maghrebi_vs_european_female_difference_of_differences   0.042437          0.0              5006.5       0.135593          238                     NaN
  maghrebi_vs_european_male_difference_of_differences  -0.042017          0.0              4855.5       0.100082          238                     NaN

### Model A1: triage level, named conditions

                                     term  coefficient  std_error  p_value    ci_low  ci_high
                                Intercept     1.246639   0.021375 0.000000  1.204743 1.288535
                    C(origin)[T.Maghrebi]    -0.042017   0.029104 0.148835 -0.099061 0.015028
                      C(gender)[T.Female]    -0.032773   0.029104 0.260143 -0.089818 0.024272
C(origin)[T.Maghrebi]:C(gender)[T.Female]     0.084454   0.041160 0.040184  0.003780 0.165127

### Model A2: triage level versus control

                                                           term  coefficient  std_error  p_value    ci_low   ci_high
                                                      Intercept     1.281092   0.022082 0.000000  1.237811  1.324374
  C(condition, Treatment(reference='control'))[T.european_male]    -0.034454   0.027579 0.211559 -0.088508  0.019601
C(condition, Treatment(reference='control'))[T.european_female]    -0.067227   0.027579 0.014784 -0.121281 -0.013173
  C(condition, Treatment(reference='control'))[T.maghrebi_male]    -0.076471   0.027579 0.005557 -0.130525 -0.022416
C(condition, Treatment(reference='control'))[T.maghrebi_female]    -0.024790   0.027579 0.368717 -0.078844  0.029264

### Logistic robustness: high urgency, level <= 2

                                                           term  coefficient  posterior_sd    ci_low  ci_high
                                                      Intercept     2.848671      0.040422  2.769444 2.927897
  C(condition, Treatment(reference='control'))[T.european_male]     0.211327      0.090104  0.034724 0.387930
C(condition, Treatment(reference='control'))[T.european_female]     0.352559      0.095835  0.164723 0.540396
  C(condition, Treatment(reference='control'))[T.maghrebi_male]     0.401063      0.097769  0.209436 0.592690
C(condition, Treatment(reference='control'))[T.maghrebi_female]     0.111656      0.086623 -0.058126 0.281438

### Model B1: named-condition entropy

                                     term  coefficient  std_error  p_value    ci_low   ci_high
                                Intercept     0.358308   0.024239 0.000000  0.310799  0.405816
                    C(origin)[T.Maghrebi]    -0.059887   0.030073 0.046433 -0.118830 -0.000945
                      C(gender)[T.Female]    -0.056523   0.030073 0.060170 -0.115465  0.002420
C(origin)[T.Maghrebi]:C(gender)[T.Female]     0.111414   0.042529 0.008800  0.028057  0.194770

### Model B2: entropy versus control

                                                           term  coefficient  std_error  p_value    ci_low   ci_high
                                                      Intercept     0.409082   0.024626 0.000000  0.360815  0.457349
  C(condition, Treatment(reference='control'))[T.european_male]    -0.050774   0.029718 0.087539 -0.109021  0.007473
C(condition, Treatment(reference='control'))[T.european_female]    -0.107297   0.029718 0.000306 -0.165544 -0.049049
  C(condition, Treatment(reference='control'))[T.maghrebi_male]    -0.110661   0.029718 0.000196 -0.168908 -0.052414
C(condition, Treatment(reference='control'))[T.maghrebi_female]    -0.055770   0.029718 0.060565 -0.114018  0.002477

### Model C: entropy x minimized urgency x origin x gender

                                                   term  coefficient  std_error  p_value    ci_low   ci_high
                                              Intercept     0.205848   0.020996 0.000000  0.164696  0.247000
                                  C(origin)[T.Maghrebi]    -0.058448   0.023953 0.014684 -0.105396 -0.011500
                                    C(gender)[T.Female]    -0.054048   0.024194 0.025488 -0.101468 -0.006627
              C(origin)[T.Maghrebi]:C(gender)[T.Female]     0.095108   0.034278 0.005526  0.027924  0.162293
                                          was_minimized     0.566961   0.035775 0.000000  0.496841  0.637080
                    was_minimized:C(origin)[T.Maghrebi]     0.063615   0.050533 0.208069 -0.035429  0.162659
                      was_minimized:C(gender)[T.Female]    -0.000351   0.049787 0.994380 -0.097933  0.097231
was_minimized:C(origin)[T.Maghrebi]:C(gender)[T.Female]    -0.100030   0.069773 0.151670 -0.236785  0.036724

## GPT-4o

Source: `raw_outputs_gpt4o.jsonl`; valid rows: 11,900; valid vignettes: 238; complete matched vignettes: 238.

### Parse-rate diagnostics

      condition  raw_rows  valid_rows  parse_success_rate  raw_vignettes  valid_vignettes
  european_male      2380        2380                 1.0            238              238
european_female      2380        2380                 1.0            238              238
  maghrebi_male      2380        2380                 1.0            238              238
maghrebi_female      2380        2380                 1.0            238              238
        control      2380        2380                 1.0            238              238

### Matched-pairs Wilcoxon tests

The four named-versus-control tests use Holm-Bonferroni correction; the two difference-of-differences tests are uncorrected.

                                           comparison  mean_diff  median_diff  wilcoxon_statistic  p_uncorrected  n_vignettes  p_holm_4_control_tests
                           maghrebi_female_vs_control  -0.013445          0.0              2589.0       0.275681          238                     1.0
                             maghrebi_male_vs_control  -0.008403          0.0              2895.5       0.348856          238                     1.0
                           european_female_vs_control  -0.003361          0.0              3054.5       0.874224          238                     1.0
                             european_male_vs_control   0.000840          0.0              2734.5       0.877307          238                     1.0
maghrebi_vs_european_female_difference_of_differences  -0.010084          0.0              2986.0       0.259928          238                     NaN
  maghrebi_vs_european_male_difference_of_differences  -0.009244          0.0              2899.5       0.167466          238                     NaN

### Model A1: triage level, named conditions

                                     term  coefficient  std_error  p_value    ci_low  ci_high
                                Intercept     2.458824   0.055307 0.000000  2.350422 2.567225
                    C(origin)[T.Maghrebi]    -0.009244   0.011750 0.431470 -0.032274 0.013787
                      C(gender)[T.Female]    -0.004202   0.011750 0.720657 -0.027232 0.018829
C(origin)[T.Maghrebi]:C(gender)[T.Female]    -0.000840   0.016617 0.959668 -0.033410 0.031730

### Model A2: triage level versus control

                                                           term  coefficient  std_error  p_value    ci_low  ci_high
                                                      Intercept     2.457983   0.061360 0.000000  2.337717 2.578250
  C(condition, Treatment(reference='control'))[T.european_male]     0.000840   0.011299 0.940712 -0.021305 0.022986
C(condition, Treatment(reference='control'))[T.european_female]    -0.003361   0.011299 0.766085 -0.025507 0.018784
  C(condition, Treatment(reference='control'))[T.maghrebi_male]    -0.008403   0.011299 0.457028 -0.030549 0.013742
C(condition, Treatment(reference='control'))[T.maghrebi_female]    -0.013445   0.011299 0.234047 -0.035591 0.008700

### Logistic robustness: high urgency, level <= 2

                                                           term  coefficient  posterior_sd    ci_low   ci_high
                                                      Intercept    -0.277841      0.038713 -0.353718 -0.201964
  C(condition, Treatment(reference='control'))[T.european_male]     0.169130      0.086752 -0.000903  0.339163
C(condition, Treatment(reference='control'))[T.european_female]     0.144890      0.086590 -0.024826  0.314605
  C(condition, Treatment(reference='control'))[T.maghrebi_male]     0.360368      0.086179  0.191458  0.529278
C(condition, Treatment(reference='control'))[T.maghrebi_female]     0.412148      0.085737  0.244103  0.580192

### Model B1: named-condition entropy

                                     term  coefficient  std_error  p_value    ci_low  ci_high
                                Intercept     0.317558   0.027723 0.000000  0.263221 0.371895
                    C(origin)[T.Maghrebi]     0.045716   0.020404 0.025059  0.005723 0.085708
                      C(gender)[T.Female]     0.054907   0.020404 0.007125  0.014915 0.094900
C(origin)[T.Maghrebi]:C(gender)[T.Female]    -0.019486   0.028856 0.499507 -0.076044 0.037073

### Model B2: entropy versus control

                                                           term  coefficient  std_error  p_value    ci_low   ci_high
                                                      Intercept     0.379528   0.027905 0.000000  0.324835  0.434221
  C(condition, Treatment(reference='control'))[T.european_male]    -0.061970   0.020616 0.002648 -0.102378 -0.021562
C(condition, Treatment(reference='control'))[T.european_female]    -0.007063   0.020616 0.731914 -0.047470  0.033345
  C(condition, Treatment(reference='control'))[T.maghrebi_male]    -0.016254   0.020616 0.430452 -0.056662  0.024153
C(condition, Treatment(reference='control'))[T.maghrebi_female]     0.019167   0.020616 0.352510 -0.021240  0.059575

### Model C: entropy x minimized urgency x origin x gender

                                                   term  coefficient  std_error  p_value    ci_low  ci_high
                                              Intercept     0.295787   0.028364 0.000000  0.240193 0.351381
                                  C(origin)[T.Maghrebi]     0.040955   0.023643 0.083234 -0.005385 0.087296
                                    C(gender)[T.Female]     0.052809   0.023540 0.024875  0.006670 0.098947
              C(origin)[T.Maghrebi]:C(gender)[T.Female]    -0.030692   0.033255 0.356042 -0.095871 0.034488
                                          was_minimized     0.090904   0.039588 0.021663  0.013310 0.168497
                    was_minimized:C(origin)[T.Maghrebi]     0.021855   0.051000 0.668269 -0.078105 0.121815
                      was_minimized:C(gender)[T.Female]     0.014300   0.051057 0.779421 -0.085772 0.114371
was_minimized:C(origin)[T.Maghrebi]:C(gender)[T.Female]     0.055270   0.072927 0.448522 -0.087667 0.198207

## Llama 3.1

Source: `raw_outputs_llama31.jsonl`; valid rows: 11,900; valid vignettes: 238; complete matched vignettes: 238.

### Parse-rate diagnostics

      condition  raw_rows  valid_rows  parse_success_rate  raw_vignettes  valid_vignettes
  european_male      2380        2380                 1.0            238              238
european_female      2380        2380                 1.0            238              238
  maghrebi_male      2380        2380                 1.0            238              238
maghrebi_female      2380        2380                 1.0            238              238
        control      2380        2380                 1.0            238              238

### Matched-pairs Wilcoxon tests

The four named-versus-control tests use Holm-Bonferroni correction; the two difference-of-differences tests are uncorrected.

                                           comparison  mean_diff  median_diff  wilcoxon_statistic  p_uncorrected  n_vignettes  p_holm_4_control_tests
                           maghrebi_female_vs_control  -0.072269        -0.05              6802.5       0.001956          238                0.005868
                             maghrebi_male_vs_control  -0.100420         0.00              5048.5       0.000115          238                0.000459
                           european_female_vs_control  -0.009244         0.00              7760.5       0.765593          238                0.765593
                             european_male_vs_control  -0.031513         0.00              6676.5       0.159095          238                0.318190
maghrebi_vs_european_female_difference_of_differences  -0.063025        -0.10              6724.0       0.001942          238                     NaN
  maghrebi_vs_european_male_difference_of_differences  -0.068908         0.00              5768.5       0.000976          238                     NaN

### Model A1: triage level, named conditions

                                     term  coefficient  std_error  p_value    ci_low   ci_high
                                Intercept     3.043277   0.077315 0.000000  2.891739  3.194815
                    C(origin)[T.Maghrebi]    -0.068908   0.020959 0.001010 -0.109988 -0.027827
                      C(gender)[T.Female]     0.022269   0.020959 0.288020 -0.018812  0.063349
C(origin)[T.Maghrebi]:C(gender)[T.Female]     0.005882   0.029641 0.842691 -0.052214  0.063979

### Model A2: triage level versus control

                                                           term  coefficient  std_error  p_value    ci_low   ci_high
                                                      Intercept     3.074790   0.077538 0.000000  2.922816  3.226764
  C(condition, Treatment(reference='control'))[T.european_male]    -0.031513   0.022405 0.159569 -0.075426  0.012400
C(condition, Treatment(reference='control'))[T.european_female]    -0.009244   0.022405 0.679915 -0.053157  0.034669
  C(condition, Treatment(reference='control'))[T.maghrebi_male]    -0.100420   0.022405 0.000007 -0.144333 -0.056507
C(condition, Treatment(reference='control'))[T.maghrebi_female]    -0.072269   0.022405 0.001257 -0.116182 -0.028356

### Logistic robustness: high urgency, level <= 2

                                                           term  coefficient  posterior_sd    ci_low   ci_high
                                                      Intercept    -1.162518      0.026893 -1.215229 -1.109807
  C(condition, Treatment(reference='control'))[T.european_male]    -0.024025      0.060332 -0.142275  0.094225
C(condition, Treatment(reference='control'))[T.european_female]    -0.074749      0.060537 -0.193401  0.043903
  C(condition, Treatment(reference='control'))[T.maghrebi_male]     0.262694      0.059576  0.145926  0.379462
C(condition, Treatment(reference='control'))[T.maghrebi_female]     0.141365      0.059885  0.023991  0.258739

### Model B1: named-condition entropy

                                     term  coefficient  std_error  p_value    ci_low  ci_high
                                Intercept     1.041357   0.036889 0.000000  0.969055 1.113660
                    C(origin)[T.Maghrebi]     0.004955   0.025152 0.843838 -0.044344 0.054253
                      C(gender)[T.Female]     0.013311   0.025152 0.596643 -0.035987 0.062610
C(origin)[T.Maghrebi]:C(gender)[T.Female]    -0.028430   0.035570 0.424146 -0.098148 0.041288

### Model B2: entropy versus control

                                                           term  coefficient  std_error  p_value    ci_low  ci_high
                                                      Intercept     1.059250   0.037140 0.000000  0.986455 1.132045
  C(condition, Treatment(reference='control'))[T.european_male]    -0.017892   0.025685 0.486045 -0.068235 0.032450
C(condition, Treatment(reference='control'))[T.european_female]    -0.004581   0.025685 0.858444 -0.054923 0.045761
  C(condition, Treatment(reference='control'))[T.maghrebi_male]    -0.012938   0.025685 0.614464 -0.063280 0.037405
C(condition, Treatment(reference='control'))[T.maghrebi_female]    -0.028056   0.025685 0.274692 -0.078398 0.022286

### Model C: entropy x minimized urgency x origin x gender

                                                   term  coefficient  std_error  p_value    ci_low  ci_high
                                              Intercept     1.000706   0.038904 0.000000  0.924455 1.076958
                                  C(origin)[T.Maghrebi]    -0.004334   0.030708 0.887750 -0.064522 0.055853
                                    C(gender)[T.Female]    -0.011142   0.031373 0.722485 -0.072633 0.050349
              C(origin)[T.Maghrebi]:C(gender)[T.Female]     0.018557   0.043754 0.671481 -0.067200 0.104314
                                          was_minimized     0.125648   0.044977 0.005213  0.037493 0.213804
                    was_minimized:C(origin)[T.Maghrebi]     0.041756   0.057872 0.470582 -0.071672 0.155185
                      was_minimized:C(gender)[T.Female]     0.054523   0.055775 0.328294 -0.054796 0.163843
was_minimized:C(origin)[T.Maghrebi]:C(gender)[T.Female]    -0.131333   0.080973 0.104818 -0.290041 0.027374

## Mistral Nemo

Source: `raw_outputs_mistral_nemo.jsonl`; valid rows: 11,900; valid vignettes: 238; complete matched vignettes: 238.

### Parse-rate diagnostics

      condition  raw_rows  valid_rows  parse_success_rate  raw_vignettes  valid_vignettes
  european_male      2380        2380                 1.0            238              238
european_female      2380        2380                 1.0            238              238
  maghrebi_male      2380        2380                 1.0            238              238
maghrebi_female      2380        2380                 1.0            238              238
        control      2380        2380                 1.0            238              238

### Matched-pairs Wilcoxon tests

The four named-versus-control tests use Holm-Bonferroni correction; the two difference-of-differences tests are uncorrected.

                                           comparison  mean_diff  median_diff  wilcoxon_statistic  p_uncorrected  n_vignettes  p_holm_4_control_tests
                           maghrebi_female_vs_control   0.002521          0.0              8139.5       0.891439          238                1.000000
                             maghrebi_male_vs_control  -0.029412          0.0              7848.5       0.298607          238                0.895820
                           european_female_vs_control   0.019328          0.0              7781.0       0.211394          238                0.845578
                             european_male_vs_control  -0.003361          0.0              7901.5       0.634751          238                1.000000
maghrebi_vs_european_female_difference_of_differences  -0.016807          0.0              7632.0       0.271607          238                     NaN
  maghrebi_vs_european_male_difference_of_differences  -0.026050          0.0              8030.0       0.067416          238                     NaN

### Model A1: triage level, named conditions

                                     term  coefficient  std_error  p_value    ci_low  ci_high
                                Intercept     2.957983   0.056406 0.000000  2.847427 3.068540
                    C(origin)[T.Maghrebi]    -0.026050   0.017625 0.139401 -0.060596 0.008495
                      C(gender)[T.Female]     0.022689   0.017625 0.197986 -0.011856 0.057234
C(origin)[T.Maghrebi]:C(gender)[T.Female]     0.009244   0.024926 0.710750 -0.039611 0.058098

### Model A2: triage level versus control

                                                           term  coefficient  std_error  p_value    ci_low  ci_high
                                                      Intercept     2.961345   0.056879 0.000000  2.849863 3.072826
  C(condition, Treatment(reference='control'))[T.european_male]    -0.003361   0.017388 0.846712 -0.037442 0.030719
C(condition, Treatment(reference='control'))[T.european_female]     0.019328   0.017388 0.266325 -0.014752 0.053408
  C(condition, Treatment(reference='control'))[T.maghrebi_male]    -0.029412   0.017388 0.090739 -0.063492 0.004668
C(condition, Treatment(reference='control'))[T.maghrebi_female]     0.002521   0.017388 0.884721 -0.031559 0.036601

### Logistic robustness: high urgency, level <= 2

                                                           term  coefficient  posterior_sd    ci_low   ci_high
                                                      Intercept    -2.033613      0.029609 -2.091648 -1.975579
  C(condition, Treatment(reference='control'))[T.european_male]    -0.063263      0.066295 -0.193200  0.066675
C(condition, Treatment(reference='control'))[T.european_female]    -0.199604      0.067703 -0.332303 -0.066906
  C(condition, Treatment(reference='control'))[T.maghrebi_male]     0.015583      0.065537 -0.112868  0.144035
C(condition, Treatment(reference='control'))[T.maghrebi_female]    -0.009375      0.065747 -0.138240  0.119490

### Model B1: named-condition entropy

                                     term  coefficient  std_error  p_value    ci_low  ci_high
                                Intercept     0.782893   0.029240 0.000000  0.725581 0.840204
                    C(origin)[T.Maghrebi]    -0.007648   0.030715 0.803357 -0.067849 0.052553
                      C(gender)[T.Female]    -0.013189   0.030715 0.667638 -0.073389 0.047012
C(origin)[T.Maghrebi]:C(gender)[T.Female]     0.013875   0.043437 0.749401 -0.071261 0.099012

### Model B2: entropy versus control

                                                           term  coefficient  std_error  p_value    ci_low  ci_high
                                                      Intercept     0.761030   0.029194 0.000000  0.703810 0.818250
  C(condition, Treatment(reference='control'))[T.european_male]     0.021863   0.030877 0.478915 -0.038657 0.082382
C(condition, Treatment(reference='control'))[T.european_female]     0.008674   0.030877 0.778773 -0.051845 0.069193
  C(condition, Treatment(reference='control'))[T.maghrebi_male]     0.014214   0.030877 0.645262 -0.046305 0.074734
C(condition, Treatment(reference='control'))[T.maghrebi_female]     0.014901   0.030877 0.629389 -0.045618 0.075420

### Model C: entropy x minimized urgency x origin x gender

                                                   term  coefficient  std_error  p_value    ci_low  ci_high
                                              Intercept     0.749627   0.034713 0.000000  0.681589 0.817665
                                  C(origin)[T.Maghrebi]     0.001342   0.040094 0.973307 -0.077242 0.079926
                                    C(gender)[T.Female]     0.004124   0.040980 0.919840 -0.076197 0.084446
              C(origin)[T.Maghrebi]:C(gender)[T.Female]     0.014615   0.057156 0.798178 -0.097411 0.126641
                                          was_minimized     0.087969   0.050167 0.079510 -0.010358 0.186296
                    was_minimized:C(origin)[T.Maghrebi]    -0.021559   0.069304 0.755741 -0.157395 0.114277
                      was_minimized:C(gender)[T.Female]    -0.051107   0.066823 0.444384 -0.182080 0.079866
was_minimized:C(origin)[T.Maghrebi]:C(gender)[T.Female]     0.001528   0.096101 0.987316 -0.186831 0.189887

## Qwen 2.5 14B

Source: `raw_outputs_qwen25_14b.jsonl`; valid rows: 11,900; valid vignettes: 238; complete matched vignettes: 238.

### Parse-rate diagnostics

      condition  raw_rows  valid_rows  parse_success_rate  raw_vignettes  valid_vignettes
  european_male      2380        2380                 1.0            238              238
european_female      2380        2380                 1.0            238              238
  maghrebi_male      2380        2380                 1.0            238              238
maghrebi_female      2380        2380                 1.0            238              238
        control      2380        2380                 1.0            238              238

### Matched-pairs Wilcoxon tests

The four named-versus-control tests use Holm-Bonferroni correction; the two difference-of-differences tests are uncorrected.

                                           comparison  mean_diff  median_diff  wilcoxon_statistic  p_uncorrected  n_vignettes  p_holm_4_control_tests
                           maghrebi_female_vs_control  -0.039916          0.0              1045.0       0.002314          238                0.003704
                             maghrebi_male_vs_control  -0.063866          0.0               916.0       0.000005          238                0.000020
                           european_female_vs_control  -0.051261          0.0              1139.0       0.000378          238                0.001133
                             european_male_vs_control  -0.044118          0.0              1182.0       0.001852          238                0.003704
maghrebi_vs_european_female_difference_of_differences   0.011345          0.0              1301.0       0.304816          238                     NaN
  maghrebi_vs_european_male_difference_of_differences  -0.019748          0.0              1238.5       0.045534          238                     NaN

### Model A1: triage level, named conditions

                                     term  coefficient  std_error  p_value    ci_low   ci_high
                                Intercept     2.371429   0.061950 0.000000  2.250006  2.492851
                    C(origin)[T.Maghrebi]    -0.019748   0.009947 0.047106 -0.039244 -0.000252
                      C(gender)[T.Female]    -0.007143   0.009947 0.472694 -0.026639  0.012353
C(origin)[T.Maghrebi]:C(gender)[T.Female]     0.031092   0.014067 0.027083  0.003521  0.058664

### Model A2: triage level versus control

                                                           term  coefficient  std_error  p_value    ci_low   ci_high
                                                      Intercept     2.415546   0.062332 0.000000  2.293376  2.537717
  C(condition, Treatment(reference='control'))[T.european_male]    -0.044118   0.011842 0.000195 -0.067327 -0.020908
C(condition, Treatment(reference='control'))[T.european_female]    -0.051261   0.011842 0.000015 -0.074470 -0.028051
  C(condition, Treatment(reference='control'))[T.maghrebi_male]    -0.063866   0.011842 0.000000 -0.087075 -0.040656
C(condition, Treatment(reference='control'))[T.maghrebi_female]    -0.039916   0.011842 0.000749 -0.063125 -0.016706

### Logistic robustness: high urgency, level <= 2

                                                           term  coefficient  posterior_sd    ci_low   ci_high
                                                      Intercept    53.728347      0.000000 53.728347 53.728347
  C(condition, Treatment(reference='control'))[T.european_male]    10.617035      0.000000 10.617035 10.617035
C(condition, Treatment(reference='control'))[T.european_female]    10.215133      0.172801  9.876443 10.553823
  C(condition, Treatment(reference='control'))[T.maghrebi_male]    10.564157      0.012437 10.539781 10.588534
C(condition, Treatment(reference='control'))[T.maghrebi_female]    10.454851      0.000010 10.454830 10.454871

### Model B1: named-condition entropy

                                     term  coefficient  std_error  p_value    ci_low  ci_high
                                Intercept     0.226913   0.023119 0.000000  0.181599 0.272227
                    C(origin)[T.Maghrebi]    -0.008714   0.018456 0.636843 -0.044888 0.027461
                      C(gender)[T.Female]    -0.003939   0.018456 0.830989 -0.040114 0.032235
C(origin)[T.Maghrebi]:C(gender)[T.Female]     0.009629   0.026101 0.712182 -0.041529 0.060788

### Model B2: entropy versus control

                                                           term  coefficient  std_error  p_value    ci_low  ci_high
                                                      Intercept     0.220476   0.023177 0.000000  0.175049 0.265903
  C(condition, Treatment(reference='control'))[T.european_male]     0.006437   0.020148 0.749367 -0.033053 0.045926
C(condition, Treatment(reference='control'))[T.european_female]     0.002497   0.020148 0.901348 -0.036992 0.041987
  C(condition, Treatment(reference='control'))[T.maghrebi_male]    -0.002277   0.020148 0.910023 -0.041767 0.037213
C(condition, Treatment(reference='control'))[T.maghrebi_female]     0.003413   0.020148 0.865469 -0.036076 0.042903

### Model C: entropy x minimized urgency x origin x gender

                                                   term  coefficient  std_error  p_value    ci_low  ci_high
                                              Intercept     0.221154   0.023247 0.000000  0.175589 0.266718
                                  C(origin)[T.Maghrebi]    -0.009361   0.019625 0.633372 -0.047825 0.029104
                                    C(gender)[T.Female]    -0.017993   0.019932 0.366663 -0.057059 0.021073
              C(origin)[T.Maghrebi]:C(gender)[T.Female]     0.004391   0.027835 0.874646 -0.050165 0.058947
                                          was_minimized     0.042834   0.046254 0.354409 -0.047823 0.133492
                    was_minimized:C(origin)[T.Maghrebi]     0.033402   0.063808 0.600640 -0.091661 0.158465
                      was_minimized:C(gender)[T.Female]     0.100061   0.056020 0.074073 -0.009739 0.209860
was_minimized:C(origin)[T.Maghrebi]:C(gender)[T.Female]     0.050231   0.085435 0.556564 -0.117220 0.217683

## Synthetic BioMistral

Source: `raw_outputs_synthetic_biomistral.jsonl`; valid rows: 10,000; valid vignettes: 200; complete matched vignettes: 200.

**DATA-QUALITY WARNING:** MODEL Synthetic BioMistral: near-random output distribution (self-consistency=0.423, entropy=1.799) — treat significance tests for this model with caution.

### Parse-rate diagnostics

      condition  raw_rows  valid_rows  parse_success_rate  raw_vignettes  valid_vignettes
  european_male      2000        2000                 1.0            200              200
european_female      2000        2000                 1.0            200              200
  maghrebi_male      2000        2000                 1.0            200              200
maghrebi_female      2000        2000                 1.0            200              200
        control      2000        2000                 1.0            200              200

### Matched-pairs Wilcoxon tests

The four named-versus-control tests use Holm-Bonferroni correction; the two difference-of-differences tests are uncorrected.

                                           comparison  mean_diff  median_diff  wilcoxon_statistic  p_uncorrected  n_vignettes  p_holm_4_control_tests
                           maghrebi_female_vs_control     0.0235          0.0              8180.5       0.648463          200                1.000000
                             maghrebi_male_vs_control     0.0950          0.1              7109.5       0.017504          200                0.070014
                           european_female_vs_control     0.0295          0.0              8072.0       0.332963          200                0.998890
                             european_male_vs_control     0.0200          0.0              8369.0       0.570603          200                1.000000
maghrebi_vs_european_female_difference_of_differences    -0.0060          0.0              8391.5       0.591400          200                     NaN
  maghrebi_vs_european_male_difference_of_differences     0.0750          0.1              7185.5       0.051858          200                     NaN

### Model A1: triage level, named conditions

                                     term  coefficient  std_error  p_value    ci_low  ci_high
                                Intercept       2.5165   0.029863 0.000000  2.457969 2.575031
                    C(origin)[T.Maghrebi]       0.0750   0.042207 0.075573 -0.007725 0.157725
                      C(gender)[T.Female]       0.0095   0.042207 0.821915 -0.073225 0.092225
C(origin)[T.Maghrebi]:C(gender)[T.Female]      -0.0810   0.059689 0.174772 -0.197991 0.035991

### Model A2: triage level versus control

                                                           term  coefficient  std_error  p_value    ci_low  ci_high
                                                      Intercept       2.4965   0.028560 0.000000  2.440522 2.552478
  C(condition, Treatment(reference='control'))[T.european_male]       0.0200   0.039357 0.611338 -0.057140 0.097140
C(condition, Treatment(reference='control'))[T.european_female]       0.0295   0.039357 0.453530 -0.047640 0.106640
  C(condition, Treatment(reference='control'))[T.maghrebi_male]       0.0950   0.039357 0.015788  0.017860 0.172140
C(condition, Treatment(reference='control'))[T.maghrebi_female]       0.0235   0.039357 0.550445 -0.053640 0.100640

### Logistic robustness: high urgency, level <= 2

                                                           term  coefficient  posterior_sd    ci_low   ci_high
                                                      Intercept     0.082833      0.019973  0.043687  0.121980
  C(condition, Treatment(reference='control'))[T.european_male]    -0.083249      0.044650 -0.170763  0.004265
C(condition, Treatment(reference='control'))[T.european_female]    -0.076890      0.044648 -0.164400  0.010621
  C(condition, Treatment(reference='control'))[T.maghrebi_male]    -0.148546      0.044668 -0.236095 -0.060997
C(condition, Treatment(reference='control'))[T.maghrebi_female]    -0.026120      0.044667 -0.113668  0.061428

### Model B1: named-condition entropy

                                     term  coefficient  std_error  p_value    ci_low  ci_high
                                Intercept     1.808718   0.019381 0.000000  1.770731 1.846705
                    C(origin)[T.Maghrebi]     0.000053   0.027159 0.998453 -0.053179 0.053285
                      C(gender)[T.Female]    -0.027036   0.027159 0.319511 -0.080268 0.026196
C(origin)[T.Maghrebi]:C(gender)[T.Female]     0.014838   0.038409 0.699261 -0.060443 0.090119

### Model B2: entropy versus control

                                                           term  coefficient  std_error  p_value    ci_low  ci_high
                                                      Intercept     1.788000   0.019461 0.000000  1.749857 1.826144
  C(condition, Treatment(reference='control'))[T.european_male]     0.020718   0.027122 0.444952 -0.032442 0.073877
C(condition, Treatment(reference='control'))[T.european_female]    -0.006318   0.027122 0.815792 -0.059478 0.046841
  C(condition, Treatment(reference='control'))[T.maghrebi_male]     0.020770   0.027122 0.443796 -0.032389 0.073930
C(condition, Treatment(reference='control'))[T.maghrebi_female]     0.008572   0.027122 0.751957 -0.044587 0.061732

### Model C: entropy x minimized urgency x origin x gender

                                                   term  coefficient  std_error  p_value    ci_low  ci_high
                                              Intercept     1.749578   0.025404 0.000000  1.699786 1.799371
                                  C(origin)[T.Maghrebi]    -0.054703   0.037098 0.140335 -0.127416 0.018010
                                    C(gender)[T.Female]    -0.022140   0.036065 0.539292 -0.092828 0.048548
              C(origin)[T.Maghrebi]:C(gender)[T.Female]     0.079508   0.052148 0.127346 -0.022702 0.181718
                                          was_minimized     0.129977   0.037612 0.000549  0.056257 0.203697
                    was_minimized:C(origin)[T.Maghrebi]     0.079006   0.052797 0.134549 -0.024477 0.182488
                      was_minimized:C(gender)[T.Female]    -0.020394   0.052681 0.698661 -0.123649 0.082860
was_minimized:C(origin)[T.Maghrebi]:C(gender)[T.Female]    -0.097187   0.074651 0.192957 -0.243502 0.049129

## Synthetic CroissantLLM

Source: `raw_outputs_synthetic_croissantllm.jsonl`; valid rows: 10,000; valid vignettes: 200; complete matched vignettes: 200.

### Parse-rate diagnostics

      condition  raw_rows  valid_rows  parse_success_rate  raw_vignettes  valid_vignettes
  european_male      2000        2000                 1.0            200              200
european_female      2000        2000                 1.0            200              200
  maghrebi_male      2000        2000                 1.0            200              200
maghrebi_female      2000        2000                 1.0            200              200
        control      2000        2000                 1.0            200              200

### Matched-pairs Wilcoxon tests

The four named-versus-control tests use Holm-Bonferroni correction; the two difference-of-differences tests are uncorrected.

                                           comparison  mean_diff  median_diff  wilcoxon_statistic  p_uncorrected  n_vignettes  p_holm_4_control_tests
                           maghrebi_female_vs_control     -0.004          0.0               852.0       0.637657          200                     1.0
                             maghrebi_male_vs_control     -0.012          0.0               796.5       0.497696          200                     1.0
                           european_female_vs_control      0.002          0.0              1019.0       0.886444          200                     1.0
                             european_male_vs_control      0.004          0.0              1207.0       0.680197          200                     1.0
maghrebi_vs_european_female_difference_of_differences     -0.006          0.0               744.0       0.652650          200                     NaN
  maghrebi_vs_european_male_difference_of_differences     -0.016          0.0               732.5       0.448156          200                     NaN

### Model A1: triage level, named conditions

                                     term  coefficient  std_error  p_value    ci_low  ci_high
                                Intercept       1.0765   0.013644 0.000000  1.049758 1.103242
                    C(origin)[T.Maghrebi]      -0.0160   0.016717 0.338502 -0.048765 0.016765
                      C(gender)[T.Female]      -0.0020   0.016717 0.904767 -0.034765 0.030765
C(origin)[T.Maghrebi]:C(gender)[T.Female]       0.0100   0.023641 0.672298 -0.036336 0.056336

### Model A2: triage level versus control

                                                           term  coefficient  std_error  p_value    ci_low  ci_high
                                                      Intercept       1.0725   0.012450 0.000000  1.048098 1.096902
  C(condition, Treatment(reference='control'))[T.european_male]       0.0040   0.017607 0.820282 -0.030510 0.038510
C(condition, Treatment(reference='control'))[T.european_female]       0.0020   0.017607 0.909562 -0.032510 0.036510
  C(condition, Treatment(reference='control'))[T.maghrebi_male]      -0.0120   0.017607 0.495524 -0.046510 0.022510
C(condition, Treatment(reference='control'))[T.maghrebi_female]      -0.0040   0.017607 0.820282 -0.038510 0.030510

### Logistic robustness: high urgency, level <= 2

                                                           term  coefficient  posterior_sd    ci_low  ci_high
                                                      Intercept     4.833260      0.082065  4.672413 4.994107
  C(condition, Treatment(reference='control'))[T.european_male]    -0.045207      0.175766 -0.389709 0.299294
C(condition, Treatment(reference='control'))[T.european_female]    -0.060756      0.173795 -0.401394 0.279882
  C(condition, Treatment(reference='control'))[T.maghrebi_male]     0.238318      0.198902 -0.151531 0.628166
C(condition, Treatment(reference='control'))[T.maghrebi_female]     0.023605      0.180895 -0.330949 0.378159

### Model B1: named-condition entropy

                                     term  coefficient  std_error  p_value    ci_low  ci_high
                                Intercept     0.108685   0.016816 0.000000  0.075726 0.141644
                    C(origin)[T.Maghrebi]    -0.008168   0.020180 0.685657 -0.047721 0.031385
                      C(gender)[T.Female]    -0.001970   0.020180 0.922234 -0.041523 0.037583
C(origin)[T.Maghrebi]:C(gender)[T.Female]    -0.000488   0.028539 0.986346 -0.056424 0.055448

### Model B2: entropy versus control

                                                           term  coefficient  std_error  p_value    ci_low  ci_high
                                                      Intercept     0.120101   0.016778 0.000000  0.087217 0.152986
  C(condition, Treatment(reference='control'))[T.european_male]    -0.011416   0.019978 0.567704 -0.050573 0.027741
C(condition, Treatment(reference='control'))[T.european_female]    -0.013386   0.019978 0.502831 -0.052543 0.025771
  C(condition, Treatment(reference='control'))[T.maghrebi_male]    -0.019584   0.019978 0.326947 -0.058741 0.019573
C(condition, Treatment(reference='control'))[T.maghrebi_female]    -0.022043   0.019978 0.269881 -0.061200 0.017115

### Model C: entropy x minimized urgency x origin x gender

                                                   term  coefficient  std_error  p_value    ci_low  ci_high
                                              Intercept     0.011882   0.011068 0.283024 -0.009811 0.033575
                                  C(origin)[T.Maghrebi]     0.024258   0.011564 0.035931  0.001592 0.046923
                                    C(gender)[T.Female]     0.017263   0.011650 0.138384 -0.005571 0.040097
              C(origin)[T.Maghrebi]:C(gender)[T.Female]    -0.016434   0.016270 0.312434 -0.048323 0.015454
                                          was_minimized     0.553160   0.021792 0.000000  0.510448 0.595872
                    was_minimized:C(origin)[T.Maghrebi]    -0.038140   0.032922 0.246659 -0.102667 0.026387
                      was_minimized:C(gender)[T.Female]    -0.018194   0.031921 0.568694 -0.080760 0.044372
was_minimized:C(origin)[T.Maghrebi]:C(gender)[T.Female]    -0.026900   0.046916 0.566399 -0.118854 0.065055

## Synthetic GPT-4o

Source: `raw_outputs_synthetic_gpt4o.jsonl`; valid rows: 10,000; valid vignettes: 200; complete matched vignettes: 200.

### Parse-rate diagnostics

      condition  raw_rows  valid_rows  parse_success_rate  raw_vignettes  valid_vignettes
  european_male      2000        2000                 1.0            200              200
european_female      2000        2000                 1.0            200              200
  maghrebi_male      2000        2000                 1.0            200              200
maghrebi_female      2000        2000                 1.0            200              200
        control      2000        2000                 1.0            200              200

### Matched-pairs Wilcoxon tests

The four named-versus-control tests use Holm-Bonferroni correction; the two difference-of-differences tests are uncorrected.

                                           comparison  mean_diff  median_diff  wilcoxon_statistic  p_uncorrected  n_vignettes  p_holm_4_control_tests
                           maghrebi_female_vs_control    -0.0120          0.0              1464.5       0.267833          200                0.848283
                             maghrebi_male_vs_control    -0.0095          0.0              1306.5       0.528334          200                1.000000
                           european_female_vs_control    -0.0140          0.0              1157.5       0.212071          200                0.848283
                             european_male_vs_control    -0.0015          0.0              1745.5       0.858483          200                1.000000
maghrebi_vs_european_female_difference_of_differences     0.0020          0.0              1362.5       0.891717          200                     NaN
  maghrebi_vs_european_male_difference_of_differences    -0.0080          0.0              1455.5       0.813687          200                     NaN

### Model A1: triage level, named conditions

                                     term  coefficient  std_error  p_value    ci_low  ci_high
                                Intercept       3.1050   0.014941 0.000000  3.075716 3.134284
                    C(origin)[T.Maghrebi]      -0.0080   0.011516 0.487249 -0.030571 0.014571
                      C(gender)[T.Female]      -0.0125   0.011516 0.277721 -0.035071 0.010071
C(origin)[T.Maghrebi]:C(gender)[T.Female]       0.0100   0.016286 0.539198 -0.021920 0.041920

### Model A2: triage level versus control

                                                           term  coefficient  std_error  p_value    ci_low  ci_high
                                                      Intercept       3.1065   0.015238 0.000000  3.076634 3.136366
  C(condition, Treatment(reference='control'))[T.european_male]      -0.0015   0.012192 0.902085 -0.025397 0.022397
C(condition, Treatment(reference='control'))[T.european_female]      -0.0140   0.012192 0.250861 -0.037897 0.009897
  C(condition, Treatment(reference='control'))[T.maghrebi_male]      -0.0095   0.012192 0.435876 -0.033397 0.014397
C(condition, Treatment(reference='control'))[T.maghrebi_female]      -0.0120   0.012192 0.325006 -0.035897 0.011897

### Logistic robustness: high urgency, level <= 2

                                                           term  coefficient  posterior_sd    ci_low   ci_high
                                                      Intercept    -8.282243      0.171641 -8.618660 -7.945827
  C(condition, Treatment(reference='control'))[T.european_male]    -0.865683      0.387747 -1.625666 -0.105700
C(condition, Treatment(reference='control'))[T.european_female]    -1.000517      0.402155 -1.788740 -0.212294
  C(condition, Treatment(reference='control'))[T.maghrebi_male]    -1.173642      0.409959 -1.977163 -0.370122
C(condition, Treatment(reference='control'))[T.maghrebi_female]    -0.403746      0.359943 -1.109234  0.301743

### Model B1: named-condition entropy

                                     term  coefficient  std_error  p_value    ci_low  ci_high
                                Intercept     0.252884   0.026400 0.000000  0.201141 0.304627
                    C(origin)[T.Maghrebi]    -0.008373   0.023090 0.716882 -0.053630 0.036884
                      C(gender)[T.Female]    -0.020096   0.023090 0.384132 -0.065352 0.025161
C(origin)[T.Maghrebi]:C(gender)[T.Female]     0.028161   0.032654 0.388476 -0.035842 0.092163

### Model B2: entropy versus control

                                                           term  coefficient  std_error  p_value    ci_low  ci_high
                                                      Intercept     0.269884   0.026527 0.000000  0.217891 0.321877
  C(condition, Treatment(reference='control'))[T.european_male]    -0.017000   0.023093 0.461636 -0.062261 0.028262
C(condition, Treatment(reference='control'))[T.european_female]    -0.037095   0.023093 0.108193 -0.082357 0.008166
  C(condition, Treatment(reference='control'))[T.maghrebi_male]    -0.025373   0.023093 0.271879 -0.070635 0.019889
C(condition, Treatment(reference='control'))[T.maghrebi_female]    -0.017308   0.023093 0.453558 -0.062570 0.027954

### Model C: entropy x minimized urgency x origin x gender

                                                   term  coefficient  std_error  p_value    ci_low  ci_high
                                              Intercept     0.149663   0.022873 0.000000  0.104831 0.194494
                                  C(origin)[T.Maghrebi]     0.016480   0.020847 0.429215 -0.024380 0.057340
                                    C(gender)[T.Female]     0.007792   0.020795 0.707892 -0.032967 0.048551
              C(origin)[T.Maghrebi]:C(gender)[T.Female]    -0.023217   0.029198 0.426510 -0.080445 0.034010
                                          was_minimized     0.480100   0.036739 0.000000  0.408091 0.552108
                    was_minimized:C(origin)[T.Maghrebi]    -0.005142   0.051486 0.920439 -0.106055 0.095770
                      was_minimized:C(gender)[T.Female]    -0.036958   0.050246 0.462001 -0.135440 0.061523
was_minimized:C(origin)[T.Maghrebi]:C(gender)[T.Female]     0.144050   0.072708 0.047569  0.001542 0.286558

## Synthetic Llama 3.1

Source: `raw_outputs_synthetic_llama31.jsonl`; valid rows: 10,000; valid vignettes: 200; complete matched vignettes: 200.

### Parse-rate diagnostics

      condition  raw_rows  valid_rows  parse_success_rate  raw_vignettes  valid_vignettes
  european_male      2000        2000                 1.0            200              200
european_female      2000        2000                 1.0            200              200
  maghrebi_male      2000        2000                 1.0            200              200
maghrebi_female      2000        2000                 1.0            200              200
        control      2000        2000                 1.0            200              200

### Matched-pairs Wilcoxon tests

The four named-versus-control tests use Holm-Bonferroni correction; the two difference-of-differences tests are uncorrected.

                                           comparison  mean_diff  median_diff  wilcoxon_statistic  p_uncorrected  n_vignettes  p_holm_4_control_tests
                           maghrebi_female_vs_control    -0.0985         -0.1              5107.0       0.000049          200                0.000139
                             maghrebi_male_vs_control    -0.1140         -0.1              4969.0       0.000046          200                0.000139
                           european_female_vs_control    -0.0815          0.0              4803.5       0.001267          200                0.001267
                             european_male_vs_control    -0.1175         -0.1              5218.5       0.000029          200                0.000115
maghrebi_vs_european_female_difference_of_differences    -0.0170          0.0              6759.0       0.428265          200                     NaN
  maghrebi_vs_european_male_difference_of_differences     0.0035          0.0              7753.0       0.958721          200                     NaN

### Model A1: triage level, named conditions

                                     term  coefficient  std_error  p_value    ci_low  ci_high
                                Intercept       4.0160   0.040302 0.000000  3.937008 4.094992
                    C(origin)[T.Maghrebi]       0.0035   0.024362 0.885763 -0.044249 0.051249
                      C(gender)[T.Female]       0.0360   0.024362 0.139481 -0.011749 0.083749
C(origin)[T.Maghrebi]:C(gender)[T.Female]      -0.0205   0.034453 0.551831 -0.088027 0.047027

### Model A2: triage level versus control

                                                           term  coefficient  std_error  p_value    ci_low   ci_high
                                                      Intercept       4.1335   0.040067 0.000000  4.054968  4.212032
  C(condition, Treatment(reference='control'))[T.european_male]      -0.1175   0.024222 0.000001 -0.164975 -0.070025
C(condition, Treatment(reference='control'))[T.european_female]      -0.0815   0.024222 0.000766 -0.128975 -0.034025
  C(condition, Treatment(reference='control'))[T.maghrebi_male]      -0.1140   0.024222 0.000003 -0.161475 -0.066525
C(condition, Treatment(reference='control'))[T.maghrebi_female]      -0.0985   0.024222 0.000048 -0.145975 -0.051025

### Logistic robustness: high urgency, level <= 2

                                                           term  coefficient  posterior_sd    ci_low   ci_high
                                                      Intercept    -6.365989      0.068692 -6.500625 -6.231353
  C(condition, Treatment(reference='control'))[T.european_male]     0.333479      0.147019  0.045322  0.621636
C(condition, Treatment(reference='control'))[T.european_female]     0.122168      0.158126 -0.187759  0.432095
  C(condition, Treatment(reference='control'))[T.maghrebi_male]     0.312574      0.148246  0.022012  0.603136
C(condition, Treatment(reference='control'))[T.maghrebi_female]     0.331101      0.147037  0.042909  0.619293

### Model B1: named-condition entropy

                                     term  coefficient  std_error  p_value    ci_low   ci_high
                                Intercept     1.249314   0.030300 0.000000  1.189925  1.308703
                    C(origin)[T.Maghrebi]    -0.044246   0.029571 0.134586 -0.102205  0.013713
                      C(gender)[T.Female]    -0.061591   0.029571 0.037268 -0.119550 -0.003632
C(origin)[T.Maghrebi]:C(gender)[T.Female]     0.012022   0.041820 0.773744 -0.069944  0.093989

### Model B2: entropy versus control

                                                           term  coefficient  std_error  p_value    ci_low  ci_high
                                                      Intercept     1.157882   0.030480 0.000000  1.098141 1.217624
  C(condition, Treatment(reference='control'))[T.european_male]     0.091432   0.030284 0.002535  0.032076 0.150788
C(condition, Treatment(reference='control'))[T.european_female]     0.029841   0.030284 0.324441 -0.029515 0.089197
  C(condition, Treatment(reference='control'))[T.maghrebi_male]     0.047186   0.030284 0.119204 -0.012170 0.106542
C(condition, Treatment(reference='control'))[T.maghrebi_female]    -0.002383   0.030284 0.937285 -0.061739 0.056973

### Model C: entropy x minimized urgency x origin x gender

                                                   term  coefficient  std_error  p_value    ci_low  ci_high
                                              Intercept     1.280726   0.034478 0.000000  1.213148 1.348304
                                  C(origin)[T.Maghrebi]    -0.008823   0.036841 0.810722 -0.081032 0.063385
                                    C(gender)[T.Female]    -0.059701   0.036875 0.105442 -0.131975 0.012573
              C(origin)[T.Maghrebi]:C(gender)[T.Female]    -0.007836   0.051731 0.879605 -0.109228 0.093557
                                          was_minimized    -0.089749   0.048734 0.065536 -0.185268 0.005771
                    was_minimized:C(origin)[T.Maghrebi]    -0.109758   0.066373 0.098197 -0.239848 0.020333
                      was_minimized:C(gender)[T.Female]    -0.006779   0.065582 0.917673 -0.135319 0.121762
was_minimized:C(origin)[T.Maghrebi]:C(gender)[T.Female]     0.055926   0.093133 0.548174 -0.126615 0.238468

## Synthetic Mistral Nemo

Source: `raw_outputs_synthetic_mistral_nemo.jsonl`; valid rows: 10,000; valid vignettes: 200; complete matched vignettes: 200.

### Parse-rate diagnostics

      condition  raw_rows  valid_rows  parse_success_rate  raw_vignettes  valid_vignettes
  european_male      2000        2000                 1.0            200              200
european_female      2000        2000                 1.0            200              200
  maghrebi_male      2000        2000                 1.0            200              200
maghrebi_female      2000        2000                 1.0            200              200
        control      2000        2000                 1.0            200              200

### Matched-pairs Wilcoxon tests

The four named-versus-control tests use Holm-Bonferroni correction; the two difference-of-differences tests are uncorrected.

                                           comparison  mean_diff  median_diff  wilcoxon_statistic  p_uncorrected  n_vignettes  p_holm_4_control_tests
                           maghrebi_female_vs_control     0.0270          0.0              6210.0       0.197176          200                0.444614
                             maghrebi_male_vs_control     0.0380          0.0              6962.5       0.270551          200                0.444614
                           european_female_vs_control     0.0505          0.0              5278.0       0.014292          200                0.057169
                             european_male_vs_control     0.0390          0.0              5961.0       0.148205          200                0.444614
maghrebi_vs_european_female_difference_of_differences    -0.0235          0.0              7059.0       0.559409          200                     NaN
  maghrebi_vs_european_male_difference_of_differences    -0.0010          0.0              7206.5       0.924227          200                     NaN

### Model A1: triage level, named conditions

                                     term  coefficient  std_error  p_value    ci_low  ci_high
                                Intercept       3.4810   0.039201 0.000000  3.404166 3.557834
                    C(origin)[T.Maghrebi]      -0.0010   0.022240 0.964136 -0.044590 0.042590
                      C(gender)[T.Female]       0.0115   0.022240 0.605096 -0.032090 0.055090
C(origin)[T.Maghrebi]:C(gender)[T.Female]      -0.0225   0.031452 0.474379 -0.084146 0.039146

### Model A2: triage level versus control

                                                           term  coefficient  std_error  p_value    ci_low  ci_high
                                                      Intercept       3.4420   0.038760 0.000000  3.366031 3.517969
  C(condition, Treatment(reference='control'))[T.european_male]       0.0390   0.022888 0.088390 -0.005860 0.083860
C(condition, Treatment(reference='control'))[T.european_female]       0.0505   0.022888 0.027356  0.005640 0.095360
  C(condition, Treatment(reference='control'))[T.maghrebi_male]       0.0380   0.022888 0.096861 -0.006860 0.082860
C(condition, Treatment(reference='control'))[T.maghrebi_female]       0.0270   0.022888 0.238135 -0.017860 0.071860

### Logistic robustness: high urgency, level <= 2

                                                           term  coefficient  posterior_sd    ci_low   ci_high
                                                      Intercept    -4.865438      0.062647 -4.988225 -4.742650
  C(condition, Treatment(reference='control'))[T.european_male]     0.293470      0.134776  0.029309  0.557630
C(condition, Treatment(reference='control'))[T.european_female]     0.030850      0.150148 -0.263439  0.325139
  C(condition, Treatment(reference='control'))[T.maghrebi_male]     0.400163      0.129256  0.146822  0.653504
C(condition, Treatment(reference='control'))[T.maghrebi_female]     0.291859      0.134759  0.027733  0.555986

### Model B1: named-condition entropy

                                     term  coefficient  std_error  p_value    ci_low  ci_high
                                Intercept     0.868120   0.030850 0.000000  0.807653 0.928586
                    C(origin)[T.Maghrebi]     0.043245   0.033816 0.200964 -0.023035 0.109524
                      C(gender)[T.Female]    -0.004569   0.033816 0.892520 -0.070849 0.061711
C(origin)[T.Maghrebi]:C(gender)[T.Female]    -0.035303   0.047823 0.460395 -0.129037 0.058431

### Model B2: entropy versus control

                                                           term  coefficient  std_error  p_value    ci_low  ci_high
                                                      Intercept     0.828221   0.031310 0.000000  0.766852 0.889589
  C(condition, Treatment(reference='control'))[T.european_male]     0.039899   0.034407 0.246210 -0.027540 0.107338
C(condition, Treatment(reference='control'))[T.european_female]     0.035330   0.034407 0.304510 -0.032109 0.102769
  C(condition, Treatment(reference='control'))[T.maghrebi_male]     0.083144   0.034407 0.015673  0.015705 0.150582
C(condition, Treatment(reference='control'))[T.maghrebi_female]     0.043271   0.034407 0.208530 -0.024167 0.110710

### Model C: entropy x minimized urgency x origin x gender

                                                   term  coefficient  std_error  p_value    ci_low  ci_high
                                              Intercept     0.780926   0.037798 0.000000  0.706842 0.855009
                                  C(origin)[T.Maghrebi]     0.067284   0.045553 0.139658 -0.021999 0.156568
                                    C(gender)[T.Female]     0.027266   0.046013 0.553462 -0.062919 0.117451
              C(origin)[T.Maghrebi]:C(gender)[T.Female]    -0.091370   0.064398 0.155945 -0.217590 0.034849
                                          was_minimized     0.202777   0.052363 0.000108  0.100145 0.305408
                    was_minimized:C(origin)[T.Maghrebi]    -0.062434   0.071512 0.382630 -0.202597 0.077729
                      was_minimized:C(gender)[T.Female]    -0.084992   0.071349 0.233566 -0.224836 0.054851
was_minimized:C(origin)[T.Maghrebi]:C(gender)[T.Female]     0.155219   0.100595 0.122828 -0.041947 0.352385

## Synthetic Qwen 2.5 14B

Source: `raw_outputs_synthetic_qwen25_14b.jsonl`; valid rows: 10,000; valid vignettes: 200; complete matched vignettes: 200.

### Parse-rate diagnostics

      condition  raw_rows  valid_rows  parse_success_rate  raw_vignettes  valid_vignettes
  european_male      2000        2000                 1.0            200              200
european_female      2000        2000                 1.0            200              200
  maghrebi_male      2000        2000                 1.0            200              200
maghrebi_female      2000        2000                 1.0            200              200
        control      2000        2000                 1.0            200              200

### Matched-pairs Wilcoxon tests

The four named-versus-control tests use Holm-Bonferroni correction; the two difference-of-differences tests are uncorrected.

                                           comparison  mean_diff  median_diff  wilcoxon_statistic  p_uncorrected  n_vignettes  p_holm_4_control_tests
                           maghrebi_female_vs_control    -0.0090          0.0               266.0       0.125205          200                0.375616
                             maghrebi_male_vs_control    -0.0140          0.0               269.5       0.053801          200                0.215203
                           european_female_vs_control     0.0035          0.0               349.5       0.756359          200                1.000000
                             european_male_vs_control    -0.0025          0.0               512.0       0.752428          200                1.000000
maghrebi_vs_european_female_difference_of_differences    -0.0125          0.0               239.0       0.050682          200                     NaN
  maghrebi_vs_european_male_difference_of_differences    -0.0115          0.0               329.5       0.119290          200                     NaN

### Model A1: triage level, named conditions

                                     term  coefficient  std_error  p_value    ci_low  ci_high
                                Intercept       2.9480   0.012769 0.000000  2.922974 2.973026
                    C(origin)[T.Maghrebi]      -0.0115   0.006583 0.080647 -0.024403 0.001403
                      C(gender)[T.Female]       0.0060   0.006583 0.362059 -0.006903 0.018903
C(origin)[T.Maghrebi]:C(gender)[T.Female]      -0.0010   0.009310 0.914460 -0.019247 0.017247

### Model A2: triage level versus control

                                                           term  coefficient  std_error  p_value    ci_low   ci_high
                                                      Intercept       2.9505   0.012815 0.000000  2.925382  2.975618
  C(condition, Treatment(reference='control'))[T.european_male]      -0.0025   0.006723 0.710010 -0.015678  0.010678
C(condition, Treatment(reference='control'))[T.european_female]       0.0035   0.006723 0.602660 -0.009678  0.016678
  C(condition, Treatment(reference='control'))[T.maghrebi_male]      -0.0140   0.006723 0.037314 -0.027178 -0.000822
C(condition, Treatment(reference='control'))[T.maghrebi_female]      -0.0090   0.006723 0.180690 -0.022178  0.004178

### Logistic robustness: high urgency, level <= 2

                                                           term  coefficient  posterior_sd    ci_low   ci_high
                                                      Intercept    -6.966371      0.059711 -7.083403 -6.849338
  C(condition, Treatment(reference='control'))[T.european_male]    -0.079403      0.134131 -0.342299  0.183493
C(condition, Treatment(reference='control'))[T.european_female]    -0.266102      0.137719 -0.536031  0.003826
  C(condition, Treatment(reference='control'))[T.maghrebi_male]     0.186667      0.129363 -0.066884  0.440218
C(condition, Treatment(reference='control'))[T.maghrebi_female]     0.041640      0.131683 -0.216459  0.299739

### Model B1: named-condition entropy

                                     term  coefficient  std_error  p_value    ci_low  ci_high
                                Intercept     0.136429   0.019884 0.000000  0.097457 0.175402
                    C(origin)[T.Maghrebi]    -0.015781   0.014819 0.286893 -0.044826 0.013263
                      C(gender)[T.Female]    -0.005143   0.014819 0.728535 -0.034188 0.023902
C(origin)[T.Maghrebi]:C(gender)[T.Female]     0.008773   0.020957 0.675492 -0.032302 0.049849

### Model B2: entropy versus control

                                                           term  coefficient  std_error  p_value    ci_low  ci_high
                                                      Intercept     0.123752   0.019986 0.000000  0.084579 0.162924
  C(condition, Treatment(reference='control'))[T.european_male]     0.012677   0.015709 0.419669 -0.018113 0.043468
C(condition, Treatment(reference='control'))[T.european_female]     0.007534   0.015709 0.631512 -0.023256 0.038325
  C(condition, Treatment(reference='control'))[T.maghrebi_male]    -0.003104   0.015709 0.843370 -0.033895 0.027687
C(condition, Treatment(reference='control'))[T.maghrebi_female]     0.000526   0.015709 0.973296 -0.030265 0.031316

### Model C: entropy x minimized urgency x origin x gender

                                                   term  coefficient  std_error  p_value    ci_low  ci_high
                                              Intercept     0.115089   0.019134 0.000000  0.077586 0.152591
                                  C(origin)[T.Maghrebi]    -0.005658   0.015445 0.714114 -0.035931 0.024614
                                    C(gender)[T.Female]    -0.005825   0.015565 0.708220 -0.036332 0.024682
              C(origin)[T.Maghrebi]:C(gender)[T.Female]     0.010415   0.021780 0.632532 -0.032275 0.053104
                                          was_minimized     0.203242   0.041423 0.000001  0.122054 0.284431
                    was_minimized:C(origin)[T.Maghrebi]    -0.030671   0.056709 0.588612 -0.141820 0.080478
                      was_minimized:C(gender)[T.Female]     0.028571   0.051026 0.575524 -0.071440 0.128583
was_minimized:C(origin)[T.Maghrebi]:C(gender)[T.Female]    -0.043336   0.080167 0.588807 -0.200464 0.113792


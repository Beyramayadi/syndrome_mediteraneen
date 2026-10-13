# FRENCH Triage Bias-Audit Results

Analysis uses only rows with `parse_success == True` and valid FRENCH levels 1-5. Lower levels are more urgent.

## Diagnostics

- Raw rows: 11,900
- Valid rows: 11,900
- Complete matched vignettes: 238

      condition  raw_rows  valid_rows  parse_success_rate  raw_vignettes  valid_vignettes
  european_male      2380        2380                 1.0            238              238
european_female      2380        2380                 1.0            238              238
  maghrebi_male      2380        2380                 1.0            238              238
maghrebi_female      2380        2380                 1.0            238              238
        control      2380        2380                 1.0            238              238

## Task 1: Matched-pairs Wilcoxon tests

Positive differences mean the named condition was less urgent than control. The four control comparisons use Holm-Bonferroni correction; difference-of-differences tests are reported uncorrected as specified.

                                           comparison  mean_diff  median_diff  wilcoxon_statistic  p_uncorrected  n_vignettes  p_holm_4_control_tests
                           maghrebi_female_vs_control  -0.024790          0.0              6350.5       0.347851          238                0.409196
                             maghrebi_male_vs_control  -0.076471          0.0              4371.0       0.002723          238                0.010892
                           european_female_vs_control  -0.067227          0.0              4883.0       0.010680          238                0.032040
                             european_male_vs_control  -0.034454          0.0              5408.0       0.204598          238                0.409196
maghrebi_vs_european_female_difference_of_differences   0.042437          0.0              5006.5       0.135593          238                     NaN
  maghrebi_vs_european_male_difference_of_differences  -0.042017          0.0              4855.5       0.100082          238                     NaN

## Model A1: triage level, named conditions

                                     term  coefficient  std_error  p_value    ci_low  ci_high
                                Intercept     1.246639   0.021375 0.000000  1.204743 1.288535
                    C(origin)[T.Maghrebi]    -0.042017   0.029104 0.148835 -0.099061 0.015028
                      C(gender)[T.Female]    -0.032773   0.029104 0.260143 -0.089818 0.024272
C(origin)[T.Maghrebi]:C(gender)[T.Female]     0.084454   0.041160 0.040184  0.003780 0.165127

## Model A2: triage level, named conditions versus control

                                                           term  coefficient  std_error  p_value    ci_low   ci_high
                                                      Intercept     1.281092   0.022082 0.000000  1.237811  1.324374
  C(condition, Treatment(reference='control'))[T.european_male]    -0.034454   0.027579 0.211559 -0.088508  0.019601
C(condition, Treatment(reference='control'))[T.european_female]    -0.067227   0.027579 0.014784 -0.121281 -0.013173
  C(condition, Treatment(reference='control'))[T.maghrebi_male]    -0.076471   0.027579 0.005557 -0.130525 -0.022416
C(condition, Treatment(reference='control'))[T.maghrebi_female]    -0.024790   0.027579 0.368717 -0.078844  0.029264

## Model A robustness: binary high urgency (level <= 2)

                                                           term  coefficient  posterior_sd    ci_low  ci_high
                                                      Intercept     2.848671      0.040422  2.769444 2.927897
  C(condition, Treatment(reference='control'))[T.european_male]     0.211327      0.090104  0.034724 0.387930
C(condition, Treatment(reference='control'))[T.european_female]     0.352560      0.095835  0.164723 0.540396
  C(condition, Treatment(reference='control'))[T.maghrebi_male]     0.401063      0.097769  0.209436 0.592691
C(condition, Treatment(reference='control'))[T.maghrebi_female]     0.111657      0.086623 -0.058125 0.281438

## Model B: Entropy/confidence disparity

## Model B1: named-condition entropy

                                     term  coefficient  std_error  p_value    ci_low   ci_high
                                Intercept     0.358308   0.024239 0.000000  0.310799  0.405816
                    C(origin)[T.Maghrebi]    -0.059887   0.030073 0.046433 -0.118830 -0.000945
                      C(gender)[T.Female]    -0.056523   0.030073 0.060170 -0.115465  0.002420
C(origin)[T.Maghrebi]:C(gender)[T.Female]     0.111414   0.042529 0.008800  0.028057  0.194770

## Model B2: entropy versus control

                                                           term  coefficient  std_error  p_value    ci_low   ci_high
                                                      Intercept     0.409082   0.024626 0.000000  0.360815  0.457349
  C(condition, Treatment(reference='control'))[T.european_male]    -0.050774   0.029718 0.087539 -0.109021  0.007473
C(condition, Treatment(reference='control'))[T.european_female]    -0.107297   0.029718 0.000306 -0.165544 -0.049049
  C(condition, Treatment(reference='control'))[T.maghrebi_male]    -0.110661   0.029718 0.000196 -0.168908 -0.052414
C(condition, Treatment(reference='control'))[T.maghrebi_female]    -0.055770   0.029718 0.060565 -0.114018  0.002477

## Model C PRIMARY RESULT: entropy x was_minimized x origin x gender

                                                   term  coefficient  std_error  p_value    ci_low   ci_high
                                              Intercept     0.205848   0.020996 0.000000  0.164696  0.247000
                                  C(origin)[T.Maghrebi]    -0.058448   0.023953 0.014684 -0.105396 -0.011500
                                    C(gender)[T.Female]    -0.054048   0.024194 0.025488 -0.101468 -0.006627
              C(origin)[T.Maghrebi]:C(gender)[T.Female]     0.095108   0.034278 0.005526  0.027924  0.162293
                                          was_minimized     0.566961   0.035775 0.000000  0.496841  0.637080
                    was_minimized:C(origin)[T.Maghrebi]     0.063615   0.050533 0.208069 -0.035429  0.162659
                      was_minimized:C(gender)[T.Female]    -0.000351   0.049787 0.994380 -0.097933  0.097231
was_minimized:C(origin)[T.Maghrebi]:C(gender)[T.Female]    -0.100030   0.069773 0.151670 -0.236785  0.036724

The PRIMARY RESULT tests whether uncertainty differs when the model minimizes urgency (`mean_level > control mean_level`) and whether that relationship varies by origin and gender. Null and non-significant terms are retained.

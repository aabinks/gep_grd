(define (problem Room_4)

(:domain navigator)
(:objects
place_8_5
place_7_11
place_13_3
place_16_3
place_9_7
place_9_10
place_15_3
place_2_3
place_9_4
place_4_3
place_10_11
place_8_10
place_3_3
place_9_11
place_6_3
place_8_4
place_8_3
place_9_8
place_5_3
place_11_11
place_12_11
place_9_5
place_7_3
place_8_6
place_16_11
place_14_11
place_15_11
place_13_11
place_8_8
place_8_9
place_4_11
place_2_11
place_9_9
place_9_6
place_6_11
place_10_3
place_5_11
place_3_11
place_9_3
place_12_3
place_11_3
place_8_11
place_14_3
place_8_7
- place
)
(:init
(connected place_8_5 place_8_4) (connected place_8_5 place_8_6) (connected place_8_5 place_9_5)
(connected place_7_11 place_6_11) (connected place_7_11 place_8_11)
(connected place_13_3 place_12_3) (connected place_13_3 place_14_3)
(connected place_16_3 place_15_3)
(connected place_9_7 place_9_6) (connected place_9_7 place_9_8) (connected place_9_7 place_8_7)
(connected place_9_10 place_9_9) (connected place_9_10 place_9_11) (connected place_9_10 place_8_10)
(connected place_15_3 place_14_3) (connected place_15_3 place_16_3)
(connected place_2_3 place_3_3)
(connected place_9_4 place_9_3) (connected place_9_4 place_9_5) (connected place_9_4 place_8_4)
(connected place_4_3 place_3_3) (connected place_4_3 place_5_3)
(connected place_10_11 place_9_11) (connected place_10_11 place_11_11)
(connected place_8_10 place_8_9) (connected place_8_10 place_8_11) (connected place_8_10 place_9_10)
(connected place_3_3 place_2_3) (connected place_3_3 place_4_3)
(connected place_9_11 place_9_10) (connected place_9_11 place_8_11) (connected place_9_11 place_10_11)
(connected place_6_3 place_5_3) (connected place_6_3 place_7_3)
(connected place_8_4 place_8_3) (connected place_8_4 place_8_5) (connected place_8_4 place_9_4)
(connected place_8_3 place_8_4) (connected place_8_3 place_7_3) (connected place_8_3 place_9_3)
(connected place_9_8 place_9_7) (connected place_9_8 place_9_9) (connected place_9_8 place_8_8)
(connected place_5_3 place_4_3) (connected place_5_3 place_6_3)
(connected place_11_11 place_10_11) (connected place_11_11 place_12_11)
(connected place_12_11 place_11_11) (connected place_12_11 place_13_11)
(connected place_9_5 place_9_4) (connected place_9_5 place_9_6) (connected place_9_5 place_8_5)
(connected place_7_3 place_6_3) (connected place_7_3 place_8_3)
(connected place_8_6 place_8_5) (connected place_8_6 place_8_7) (connected place_8_6 place_9_6)
(connected place_16_11 place_15_11)
(connected place_14_11 place_13_11) (connected place_14_11 place_15_11)
(connected place_15_11 place_14_11) (connected place_15_11 place_16_11)
(connected place_13_11 place_12_11) (connected place_13_11 place_14_11)
(connected place_8_8 place_8_7) (connected place_8_8 place_8_9) (connected place_8_8 place_9_8)
(connected place_8_9 place_8_8) (connected place_8_9 place_8_10) (connected place_8_9 place_9_9)
(connected place_4_11 place_3_11) (connected place_4_11 place_5_11)
(connected place_2_11 place_3_11)
(connected place_9_9 place_9_8) (connected place_9_9 place_9_10) (connected place_9_9 place_8_9)
(connected place_9_6 place_9_5) (connected place_9_6 place_9_7) (connected place_9_6 place_8_6)
(connected place_6_11 place_5_11) (connected place_6_11 place_7_11)
(connected place_10_3 place_9_3) (connected place_10_3 place_11_3)
(connected place_5_11 place_4_11) (connected place_5_11 place_6_11)
(connected place_3_11 place_2_11) (connected place_3_11 place_4_11)
(connected place_9_3 place_9_4) (connected place_9_3 place_8_3) (connected place_9_3 place_10_3)
(connected place_12_3 place_11_3) (connected place_12_3 place_13_3)
(connected place_11_3 place_10_3) (connected place_11_3 place_12_3)
(connected place_8_11 place_8_10) (connected place_8_11 place_7_11) (connected place_8_11 place_9_11)
(connected place_14_3 place_13_3) (connected place_14_3 place_15_3)
(connected place_8_7 place_8_6) (connected place_8_7 place_8_8) (connected place_8_7 place_9_7) (at place_8_7)
(is_free place_8_5)
(is_free place_7_11)
(is_free place_13_3)
(is_free place_16_3)
(is_free place_9_7)
(is_free place_9_10)
(is_free place_15_3)
(is_free place_2_3)
(is_free place_9_4)
(is_free place_4_3)
(is_free place_10_11)
(is_free place_8_10)
(is_free place_3_3)
(is_free place_9_11)
(is_free place_6_3)
(is_free place_8_4)
(is_free place_8_3)
(is_free place_9_8)
(is_free place_5_3)
(is_free place_11_11)
(is_free place_12_11)
(is_free place_9_5)
(is_free place_7_3)
(is_free place_8_6)
(is_free place_16_11)
(is_free place_14_11)
(is_free place_15_11)
(is_free place_13_11)
(is_free place_8_8)
(is_free place_8_9)
(is_free place_4_11)
(is_free place_2_11)
(is_free place_9_9)
(is_free place_9_6)
(is_free place_6_11)
(is_free place_10_3)
(is_free place_5_11)
(is_free place_3_11)
(is_free place_9_3)
(is_free place_12_3)
(is_free place_11_3)
(is_free place_8_11)
(is_free place_14_3)
(is_free place_8_7)
)
(:goal
(and
<HYPOTHESIS>
)
)
)

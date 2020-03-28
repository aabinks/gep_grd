(define (problem Simple_Room_2)

(:domain navigator)
(:objects
place_15_6
place_14_6
place_19_6
place_2_8
place_6_10
place_6_7
place_16_6
place_2_3
place_10_5
place_10_6
place_6_3
place_17_6
place_2_7
place_10_9
place_7_6
place_6_6
place_12_6
place_11_6
place_10_4
place_6_9
place_13_6
place_2_5
place_10_10
place_2_6
place_10_8
place_6_5
place_2_9
place_4_6
place_3_6
place_9_6
place_10_3
place_6_8
place_2_4
place_8_6
place_5_6
place_18_6
place_2_10
place_10_7
place_6_4
- place
)
(:init
(connected place_15_6 place_14_6) (connected place_15_6 place_16_6)
(connected place_14_6 place_13_6) (connected place_14_6 place_15_6)
(connected place_19_6 place_18_6) (at place_19_6)
(connected place_2_8 place_2_7) (connected place_2_8 place_2_9)
(connected place_6_10 place_6_9)
(connected place_6_7 place_6_6) (connected place_6_7 place_6_8)
(connected place_16_6 place_15_6) (connected place_16_6 place_17_6)
(connected place_2_3 place_2_4)
(connected place_10_5 place_10_4) (connected place_10_5 place_10_6)
(connected place_10_6 place_10_5) (connected place_10_6 place_10_7) (connected place_10_6 place_9_6) (connected place_10_6 place_11_6)
(connected place_6_3 place_6_4)
(connected place_17_6 place_16_6) (connected place_17_6 place_18_6)
(connected place_2_7 place_2_6) (connected place_2_7 place_2_8)
(connected place_10_9 place_10_8) (connected place_10_9 place_10_10)
(connected place_7_6 place_6_6) (connected place_7_6 place_8_6)
(connected place_6_6 place_6_5) (connected place_6_6 place_6_7) (connected place_6_6 place_5_6) (connected place_6_6 place_7_6)
(connected place_12_6 place_11_6) (connected place_12_6 place_13_6)
(connected place_11_6 place_10_6) (connected place_11_6 place_12_6)
(connected place_10_4 place_10_3) (connected place_10_4 place_10_5)
(connected place_6_9 place_6_8) (connected place_6_9 place_6_10)
(connected place_13_6 place_12_6) (connected place_13_6 place_14_6)
(connected place_2_5 place_2_4) (connected place_2_5 place_2_6)
(connected place_10_10 place_10_9)
(connected place_2_6 place_2_5) (connected place_2_6 place_2_7) (connected place_2_6 place_3_6)
(connected place_10_8 place_10_7) (connected place_10_8 place_10_9)
(connected place_6_5 place_6_4) (connected place_6_5 place_6_6)
(connected place_2_9 place_2_8) (connected place_2_9 place_2_10)
(connected place_4_6 place_3_6) (connected place_4_6 place_5_6)
(connected place_3_6 place_2_6) (connected place_3_6 place_4_6)
(connected place_9_6 place_8_6) (connected place_9_6 place_10_6)
(connected place_10_3 place_10_4)
(connected place_6_8 place_6_7) (connected place_6_8 place_6_9)
(connected place_2_4 place_2_3) (connected place_2_4 place_2_5)
(connected place_8_6 place_7_6) (connected place_8_6 place_9_6)
(connected place_5_6 place_4_6) (connected place_5_6 place_6_6)
(connected place_18_6 place_17_6) (connected place_18_6 place_19_6)
(connected place_2_10 place_2_9)
(connected place_10_7 place_10_6) (connected place_10_7 place_10_8)
(connected place_6_4 place_6_3) (connected place_6_4 place_6_5)
(is_free place_15_6)
(is_free place_14_6)
(is_free place_19_6)
(is_free place_2_8)
(is_free place_6_10)
(is_free place_6_7)
(is_free place_16_6)
(is_free place_2_3)
(is_free place_10_5)
(is_free place_10_6)
(is_free place_6_3)
(is_free place_17_6)
(is_free place_2_7)
(is_free place_10_9)
(is_free place_7_6)
(is_free place_6_6)
(is_free place_12_6)
(is_free place_11_6)
(is_free place_10_4)
(is_free place_6_9)
(is_free place_13_6)
(is_free place_2_5)
(is_free place_10_10)
(is_free place_2_6)
(is_free place_10_8)
(is_free place_6_5)
(is_free place_2_9)
(is_free place_4_6)
(is_free place_3_6)
(is_free place_9_6)
(is_free place_10_3)
(is_free place_6_8)
(is_free place_2_4)
(is_free place_8_6)
(is_free place_5_6)
(is_free place_18_6)
(is_free place_2_10)
(is_free place_10_7)
(is_free place_6_4)
)
(:goal
(and
(at place_2_10)
)
)
)

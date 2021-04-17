module Main where

song :: Int -> String
song n = if n==0 then ""
	 else song (n-1) ++ "\n" ++ verse n

verse n = line1 n ++ line2 n ++ line3 n ++ line4 n

line1 n = intToNumMenUpper !! (n-1) ++ " went to mow\n"
line2 n = intToNumMenUpper !! (n-1) ++ " went to mow a meadow\n"
line3 n = intToNumMenUpper !! (n-1) ++ ", " ++  menCountdown (n-1) 0 ++ "and his dog\n" 
line4 n = "Went to mow a meadow\n"

menCountdown :: Int -> Int ->  String
menCountdown n counter  = if n < counter  then ""
		 	  else menCountdown n (counter+1)  ++ intToNumMenLower !! counter ++ ", "

intToNumMenUpper = ["One man", "Two men", "Three men", "Four men", "Five men", "Six men", "Seven men", "Eight men", "Nine men"]
intToNumMenLower= ["one man", "two men", "three men", "four men", "five men", "six men", "seven men", "eight men", "nine men"]

mapInput n | n <= 0 = main
	   | n > 0 && n <= 9 = putStrLn $ song n
	   | n > 9 = main

main :: IO ()
main =  do
	putStrLn "How many men are there (0 < input <= 9)"
	numMen <- getLine
	let numMenInt = (read numMen :: Int)
        mapInput (numMenInt)

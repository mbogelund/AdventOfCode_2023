/* AoC 2023 */
/* Dec07 */

%put &=sysscp;
%if %sysfunc(substr(&sysscp., 1, 3)) = WIN %then %do;
  %let execPgmPath=%sysget(SAS_EXECFILEPATH); * Hvor ligger dette SAS-program der eksekveres lige nu? ;
  %let pdlm=\;
%end;
%if %sysfunc(substr(&sysscp., 1, 3)) = LIN %then %do;
  %let execPgmPath=&_SASPROGRAMFILE.; * Hvor ligger dette SAS-program der eksekveres lige nu? ;
  %let pdlm=/;
%end;
%put &=pdlm;

%let execPgm=%sysfunc(scan(&execPgmPath.,-1,&pdlm.));
%let execPath=%sysfunc(substr(&execPgmPath., 1, %sysfunc(length(&execPgmPath.)) - %sysfunc(length(&execPgm.))));

%put &=execPgmPath;
%put &=execPgm;
%put &=execPath;

libname dat "&execPath.data";

/* Import raw input */
filename in_file "&execPath.Input&pdlm.input.txt";
*filename in_file "&execPath.Input&pdlm.example.txt";
data WORK.input;
  length inline $ 1024;
  infile in_file;
  input;
  inline = trim(left(_INFILE_));
run;
filename in_file clear;

proc sql NOPRINT;
  select max(length(inline)) into :max_length
  from WORK.input
  ;
  select count(*) into :count_rows
  from WORK.input
  ;
quit;
%put &=max_length;
%put &=count_rows;

/* Part 1 */


data  WORK.CARDS;
  length card_label        $   1
         card_match_string $  14
  ;
  drop card_string
       card_match_string
       idx
  ;
  card_match_string = '';
  card_string = "A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2";
  card_label = scan(card_string, 1, ', ');
  do idx=2 to 100 while (card_label ^= '');
    card_match_string = card_label || compress(card_match_string);
    card_strength = 16 - idx;
    output;
    card_label = scan(card_string, idx, ', ');
  end;
  card_match_string = '¤' || compress(card_match_string);
  call symput('card_match_string', card_match_string);
run;
%put &=card_match_string;

data WORK.HAND_TYPES;
  length configuration_string $ 5
         hand_strength          8
  ;
  retain hand_strength 0;
  input configuration_string $;
  hand_strength = hand_strength +1;
cards;
1111
2111
221
311
32
41
5
run;

data WORK.CARDS_ARRAY;
  set WORK.CARDS end=last;
  retain L1-L14;
  keep L1-L14;
  array CARD_LABELS(14) $ L1-L14;
  CARD_LABELS(card_strength) = card_label;
  if last then output;
run;

data WORK.HANDS_AND_BIDS;
  set WORK.INPUT;
  length hand                 $ 5
         hand_sorted          $ 5
         configuration_string $ 5
         bid                    8
         ;
  array strength{5}               S1-S5;
  array strength_sorted{5}        SS1-SS5;
  array configuration{5}          C1-C5;
  array configuration_sorted{5}   CS1-CS5;
  hand = scan(INLINE, 1, ' ');*hand='23456';
  bid = input(scan(INLINE, 2, ' '), 16.);
  do idx = 1 to length(hand);
    strength(idx) = index("&card_match_string.", substr(hand, idx, 1));
    if idx=1 then do;
      strength_sorted(length(hand) + 1 - idx) = strength(idx);
    end;
    else do;
      strength_sorted(length(hand) + 1 - idx) = strength(idx);
      do idx2 = length(hand) + 1 - idx to length(hand) - 1;  
        if strength_sorted(idx2) < strength_sorted(idx2 + 1) then do;
            strength_sorted(idx2) = strength_sorted(idx2 + 1);
            strength_sorted(idx2 + 1) = strength(idx);
        end;
      end;
    end;
    *output;
  end;

  repeat = 1;
  idx2 = 1;
  do idx = 2 to length(hand);
    if strength_sorted(idx-1) = strength_sorted(idx) then do;
      repeat = repeat + 1;
    end;
    else do;
      configuration(idx2) = repeat;
      idx2 = idx2 + 1;
      repeat = 1;
    end;
    configuration(idx2) = repeat;   
    *output;
  end;
  do idx = 1 to length(hand);
    configuration_sorted(length(hand) + 1 - idx) = configuration(idx);
    do idx2 = length(hand) + 1 - idx to length(hand) - 1;  
      if configuration_sorted(idx2) < configuration_sorted(idx2 + 1) then do;
          configuration_sorted(idx2) = configuration_sorted(idx2 + 1);
          configuration_sorted(idx2 + 1) = configuration(idx);
      end;
    end;
  end;

  do idx = 1 to length(hand);
    if configuration_sorted(idx) ^= . then do;
      configuration_string = compress(configuration_string) || compress(put(configuration_sorted(idx), 16.));
    end;
    hand_sorted = compress(hand_sorted) || substr("&card_match_string.", strength_sorted(idx), 1);
  end;
run;

proc sql;
  create table WORK.HAND_STRENGTH as
  select h.INLINE,
         h.HAND,
         h.HAND_SORTED,
         h.CONFIGURATION_STRING,
         t.HAND_STRENGTH,
         h.BID,
         h.S1,
         h.S2,
         h.S3,
         h.S4,
         h.S5
  from WORK.HANDS_AND_BIDS h
  LEFT JOIN WORK.HAND_TYPES t
    on h.CONFIGURATION_STRING = t.CONFIGURATION_STRING
  order by HAND_STRENGTH , S1, S2, S3, S4, S5
  ;
quit;

data WORK.HAND_RANK_AND_WINNING;
  set WORK.HAND_STRENGTH;
  RANK = _N_;
  WINNING = BID * RANK;
run;

proc sql;
  create table WORK.TOTAL_WINNINGS as
  select sum(WINNING) as part_1_answer
  from WORK.HAND_RANK_AND_WINNING
  ;
quit;

data WORK.PART1;
  set WORK.TOTAL_WINNINGS(obs=1);
  put 'Answer to part 1: ' part_1_answer;
run;

/* Result: 252295678 */
/* Evaluation: Correct! */


/* Part 2? */


/* Result:  */
/* Evaluation:  */

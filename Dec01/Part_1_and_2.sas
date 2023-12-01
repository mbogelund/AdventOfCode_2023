/* AoC 2023 */
/* Dec01 */

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

/* Part 1 */
filename in_file "&execPath.Input&pdlm.input.txt";
data WORK.input;
  length inline $ 1024;
  infile in_file;
  input;
  inline = compress(_INFILE_);
run;
filename in_file clear;

proc sql NOPRINT;
  select max(length(inline)) into: max_length
  from WORK.input
  ;
quit;
%put &=max_length;

data WORK.scan;
  set input;
  length num_digit_string         $ &max_length.
         compact_num_digit_string $ &max_length.
         c_two_digits             $ 2
         n_two_digits               8
  ;
  array num_digit{10}  $ n0-n9  ('0' '1' '2' '3' '4' '5' '6' '7' '8' '9');
  do i=0 to 9;
    idx = find(lowcase(inline), trim(left(num_digit{i+1})));
    do while (idx > 0);
      substr(num_digit_string, idx, 1) = num_digit{i+1};
      idx = find(lowcase(inline), trim(left(num_digit{i+1})), idx+1);
    end;
  end;

  compact_num_digit_string = compress(num_digit_string);
  substr(c_two_digits, 1, 1) = substr(compact_num_digit_string, 1, 1);
  substr(c_two_digits, 2, 1) = substr(compact_num_digit_string, length(compact_num_digit_string), 1);
  n_two_digits = input(c_two_digits, 2.);
run;

proc sql;
  create table WORK.SUM_CALIBRATION_VALUES as
  select sum(n_two_digits) as CAL_SUM
  from WORK.scan
  ;
quit;

data WORK.PART1;
  set WORK.SUM_CALIBRATION_VALUES(obs=1);
  put 'Sum of calibration values: ' CAL_SUM;
run;


/* Part 2*/

data WORK.scan;
  set input;
  length num_digit_string         $ &max_length.
         compact_num_digit_string $ &max_length.
         c_two_digits             $ 2
         n_two_digits               8
  ;
  array word_digit{10} $ w0-w9  ('zero' 'one' 'two' 'three' 'four' 'five' 'six' 'seven' 'eight' 'nine');
  array num_digit{10}  $ n0-n9  ('0' '1' '2' '3' '4' '5' '6' '7' '8' '9');
  do i=0 to 9;
    idx = find(lowcase(inline), trim(left(word_digit{i+1})));
    do while (idx > 0);
      substr(num_digit_string, idx, 1) = num_digit{i+1};
      idx = find(lowcase(inline), trim(left(word_digit{i+1})), idx+1);
    end;
    idx = find(lowcase(inline), trim(left(num_digit{i+1})));
    do while (idx > 0);
      substr(num_digit_string, idx, 1) = num_digit{i+1};
      idx = find(lowcase(inline), trim(left(num_digit{i+1})), idx+1);
    end;
  end;

  compact_num_digit_string = compress(num_digit_string);
  substr(c_two_digits, 1, 1) = substr(compact_num_digit_string, 1, 1);
  substr(c_two_digits, 2, 1) = substr(compact_num_digit_string, length(compact_num_digit_string), 1);
  n_two_digits = input(c_two_digits, 2.);
run;

proc sql;
  create table WORK.SUM_CALIBRATION_VALUES as
  select sum(n_two_digits) as CAL_SUM
  from WORK.scan
  ;
quit;

data WORK.PART1;
  set WORK.SUM_CALIBRATION_VALUES(obs=1);
  put 'Sum of calibration values: ' CAL_SUM;
run;

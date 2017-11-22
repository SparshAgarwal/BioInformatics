# set up testing enviroments
PATH=/s/bin:/usr/lib64/qt-3.3/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/bin
PATH=/s/pkg/linux64/gcc/4.8.4/bin:$PATH # use c++11

# TASK_NAME="forward"

# choose the timeout command depending on OS
case "$(uname -s)" in
    Linux*)     CMD_TIMEOUT=timeout;;
    Darwin*)    CMD_TIMEOUT=gtimeout;;
    *)          CMD_TIMEOUT="UNKNOWN"
esac
MAX_TIME=1

# take students either from args or from file
if [ $# > 0 ]; then 
    STUDENT_IDS=$@
else
    STUDENT_IDS=$(cat students)
fi

TEST_CASES_DIR=$(pwd)/test_cases


TEST_CASES=(1 2 3 4 5 6 7)
N_STATES=(2 4 4 3 4 5 6)
TEST_SEQS=(TAG TAG TAGC ATGT CCCCGACACCACA TCCCCTGCTATCTGCTCTCGA TCTAGTAAGCCCCCGTTGACCTGACGCGACAAATCACGCGAAAAAGGCACGCGGATTCACGATGGGGGGCGCACGCCA)
[ ${#TEST_CASES[@]} -eq ${#N_STATES[@]} ] || echo "TEST_CASES and N_STATES don't have an equal length. "
[ ${#TEST_CASES[@]} -eq ${#TEST_SEQS[@]} ] || echo "TEST_CASES and TEST_SEQS don't have an equal length. "

WORKSPACE=$(pwd)


my_diff () {
    # Compare two files's content, ignoring blank lines, trailing ctr and
    # adding newline if there isn't one

    # add newline if there isn't one
    output1=$(sed -e '$a\' $1)
    output2=$(sed -e '$a\' $2)

    diff --ignore-blank-lines --strip-trailing-cr <(echo $output1) <(echo $output2)
}


echo "--------------------"

# clean up temporal files
ls | grep -E "\.(class|out|jar)" | xargs rm -rf
ls | grep -E "^${TASK_NAME}$" | xargs rm -rf
ls | grep -E "^output.*\.txt$" | xargs rm -rf

# Compile source codes
source_files=$(ls | grep -E "\.(c|cpp|cxx|java|R|py)$")
# echo $source_files
if [[ $source_files =~ .*\.java$ ]]; then
    { # catch
        # javac *.java
        bash compile.sh
    } || { # except
        echo "Compiling Error: $source_files !"
        continue
    }
elif [[ $source_files =~ .*\.(cpp|cxx|c)$ ]]; then
    { # catch
        # g++ --std=c++11 *.c* -o ${TASK_NAME}
        bash compile.sh
    } || { # except
        echo "Compiling Error: $source_files !"
        continue
    }
fi

for task_name in forward viterbi; do
    echo "$task_name:"

    # run and test
    if [[ ! -f ${task_name}.sh ]]; then
        echo "Execution wrapper file not exist."
        continue
    fi

    for (( i = 0; i < ${#TEST_CASES[@]}; i++ )); do
        test_case=${TEST_CASES[$i]}
        n_state=${N_STATES[$i]}
        test_seq=${TEST_SEQS[$i]}

        T_INPUT=$TEST_CASES_DIR/transition${test_case}.txt
        E_INPUT=$TEST_CASES_DIR/emission${test_case}.txt

        OUTPUT=${task_name}${test_case}.txt

        if [[ -f $OUTPUT ]]; then
            rm $OUTPUT
        fi

        { # similar to a 'try' block
            $CMD_TIMEOUT $MAX_TIME bash ${task_name}.sh $n_state $T_INPUT $E_INPUT $test_seq > $OUTPUT 2>&1
        } || { # your 'catch' block
            if [[ -s $OUTPUT ]]; then
                echo "RE: test case $test_case"
                echo -e "$(cat $OUTPUT)\n"
            else
                echo "Timeout: test case $test_case !"
            fi
            continue
        }


        if my_diff $OUTPUT $TEST_CASES_DIR/$OUTPUT ; then
            echo "AC: test case $test_case !"
        else
            echo "WA: test case $test_case !"
        fi

    done
done

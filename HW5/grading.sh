# set up testing enviroments
PATH=/s/bin:/usr/lib64/qt-3.3/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/bin
PATH=/s/pkg/linux64/gcc/4.8.4/bin:$PATH # use c++11

TASK_NAME="cluster"

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


TEST_CASES=(1 2 3 4 5 6 7 8 9)
CLUSTER_SIZES=(2 2 2 4 4 4 6 6 6)
DATA=(tiny tiny tiny tiny tiny tiny tiny tiny tiny)
TYPES=(S C A S C A S C A)

[ ${#TEST_CASES[@]} -eq ${#CLUSTER_SIZES[@]} ] || echo "TEST_CASES and CLUSTER_SIZES don't have an equal length. "
[ ${#TEST_CASES[@]} -eq ${#DATA[@]} ] || echo "TEST_CASES and DATA don't have an equal length. "
[ ${#TEST_CASES[@]} -eq ${#TYPES[@]} ] || echo "TEST_CASES and TYPES don't have an equal length. "

WORKSPACE=$(pwd)


my_diff () {
    # Compare two files's content, ignoring blank lines, trailing ctr and
    # adding newline if there isn't one

    # add newline if there isn't one
    output1=$(sed -e '$a\' $1)
    output2=$(sed -e '$a\' $2)

    diff --ignore-blank-lines --strip-trailing-cr <(echo $output1) <(echo $output2)
}



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


# run and test
if [[ ! -f ${TASK_NAME}.sh ]]; then
    echo "Execution wrapper file not exist."
    continue
fi

for (( i = 0; i < ${#TEST_CASES[@]}; i++ )); do

    test_case=${TEST_CASES[$i]}
    data_name=${DATA[$i]}
    type=${TYPES[$i]}
    k=${CLUSTER_SIZES[$i]}

    INPUT=$TEST_CASES_DIR/${data_name}-yeast.tsv
    OUTPUT=${data_name}-$type-$k.txt

    if [[ -f $OUTPUT ]]; then
        rm $OUTPUT
    fi

    { # similar to a 'try' block
        start_time=$(date +%s%N)
        $CMD_TIMEOUT $MAX_TIME bash ${TASK_NAME}.sh $INPUT $type $k > $OUTPUT 2>&1
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
        end_time=$(date +%s%N)
        echo "AC: test case $test_case ! Time taken: $(bc <<< "scale=2; ($end_time - $start_time) / 1000000000 " ) s"
    else
        echo "WA: test case $test_case !"
    fi

done

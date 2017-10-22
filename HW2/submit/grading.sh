# set up testing enviroments
PATH=/s/bin:/usr/lib64/qt-3.3/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/bin
PATH=/s/pkg/linux64/gcc/4.8.4/bin:$PATH # use c++11

TASK_NAME="anchor_alignment"

# choose the timeout command depending on OS
case "$(uname -s)" in
    Linux*)     CMD_TIMEOUT=timeout;;
    Darwin*)    CMD_TIMEOUT=gtimeout;;
    *)          CMD_TIMEOUT="UNKNOWN"
esac
MAX_TIME=10

TEST_CASES_DIR=$(pwd)/test_cases
# set the test case name for testing; seperated by space
TEST_CASES="1 2 3 4 5 6 7 8"

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

# compile source codes
source_files=$(ls | grep -E "\.(c|cpp|cxx|java|R|py)$")
# echo $source_files
if [[ $source_files =~ .*\.java$ ]]; then
    { # catch
        # javac *.java
        bash compile.sh
    } || { # except
        echo "Compiling Error: $source_files !"
    }
elif [[ $source_files =~ .*\.(cpp|cxx|c)$ ]]; then
    { # catch
        # g++ --std=c++11 *.c* -o ${TASK_NAME}
        bash compile.sh
    } || { # except
        echo "Compiling Error: $source_files !"
    }
fi

# run and test
if [[ ! -f ${TASK_NAME}.sh ]]; then
    echo "Execution wrapper file not exist."
fi

for test_case in $TEST_CASES; do
    INPUT=$TEST_CASES_DIR/input${test_case}.txt
    OUTPUT=output${test_case}.txt

    if [[ -f $OUTPUT ]]; then
        rm $OUTPUT
    fi

    { # similar to a 'try' block
        $CMD_TIMEOUT $MAX_TIME bash ${TASK_NAME}.sh $INPUT > $OUTPUT 2>&1
    } || { # your 'catch' block
        if [[ -s $OUTPUT ]]; then
            echo "RE: test case $test_case"
            echo -e "$(cat $OUTPUT)\n"
        else
            echo "Timeout: test case $test_case"
        fi
        continue
    }


    if my_diff $OUTPUT $TEST_CASES_DIR/$OUTPUT ; then
        echo "AC: test case $test_case"
    else
        echo "WA: test case $test_case"
    fi

done

echo -e "--------------------\n"

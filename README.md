# practise

To write the programme was used Python 3.13 on Windows.

This is a console programme for testing server availability via HTTP protocol.  The programme measures the request execution time and outputs the final statistics on the server response speed.

HOW to use:
1) Install all dependencies from requirements.txt 
    "pip install -r requirements.txt"

2) Type ‘python bench.py --help’ to view all available commands

Examples of input and output:

    input: "python bench.py -H https://vk.com -C 5"
    output: Host = https://vk.com
            Success = 5
            Failed = 0
            Errors = 0
            Min = 0.525694 seconds
            Max = 0.562843 seconds
            Avg = 0.540661 seconds

    input: "python bench.py -F .\site.txt -C 5 -O .\output.txt"
    output: in file "output.txt"

    input: "python bench.py -H https://ya.ru,https://vk.com -C 10"
    output: Host = https://ya.ru
            Success = 10
            Failed = 0
            Errors = 0
            Min = 0.249481 seconds
            Max = 0.341880 seconds
            Avg = 0.291739 seconds

            Host = https://vk.com
            Success = 10
            Failed = 0
            Errors = 0
            Min = 0.497386 seconds
            Max = 0.544228 seconds
            Avg = 0.524620 seconds

    
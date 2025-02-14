import asyncio
import aiohttp
import argparse


class Counter:
    Counts = 0

    def __new__(cls):
        cls.Counts += 1
        return super().__new__(cls)

    @classmethod
    def get_count(cls):
        return cls.Counts

    @classmethod
    def clear(cls):
        cls.Counts = 0


class CounterERROR(Counter):
    pass


class CounterSUCCES(Counter):
    pass


class CounterFAILED(Counter):
    pass


class CreateResult:
    result = str()

    @classmethod
    def add(cls, url, time_responses):
        if time_responses:
            avg = sum(time_responses) / len(time_responses)
            cls.result += (f'''Host = {url}
Success = {CounterSUCCES.get_count()}
Failed = {CounterFAILED.get_count()}
Errors = {CounterERROR.get_count()}
Min = {min(time_responses):.6f} seconds
Max = {max(time_responses):.6f} seconds
Avg = {avg:.6f} seconds

''')
            time_responses.clear()
            CounterERROR.clear()
            CounterFAILED.clear()
            CounterSUCCES.clear()
        else:
            cls.result += (f'''Host = {url}
Success = {CounterSUCCES.get_count()}
Failed = {CounterFAILED.get_count()}
Errors = {CounterERROR.get_count()}
Min = {None} seconds
Max = {None} seconds
Avg = {None} seconds

''')

    @classmethod
    def get(cls):
        return cls.result


def GUI():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-H', '--hosts', help="Host addresses. Use '--hosts' or '--file'")
    parser.add_argument('-C', '--count', help="Number of requests", type=int)
    parser.add_argument(
        '-F', '--file', help="Path to the file with the list of addresses divided into lines")
    parser.add_argument(
        '-O', '--output', help="Path to the file where you want to save the output")
    args = parser.parse_args()
    validator(args)
    return args


def validator(args):
    if not args.hosts and not args.file:
        raise AttributeError('No addresses for testing. Use "--help"')
    elif args.hosts and args.file:
        raise AttributeError(
            'These arguments cannot be used in pairs. Use "--help"')


def get_parametrs():
    args = GUI()
    urls = []
    count = 1
    if args.hosts:
        urls = args.hosts.split(',')
    else:
        with open(args.file) as file:
            for url in file.readlines():
                urls.append(url.rstrip('\n'))
    if args.count:
        count = args.count
    if args.output:
        output = args.output
    else:
        output = False
    return urls, count, output


async def on_request_start(session, trace_config_ctx, params):
    trace_config_ctx.start = asyncio.get_event_loop().time()


async def on_request_end(session, trace_config_ctx, params):
    elapsed = asyncio.get_event_loop().time() - trace_config_ctx.start
    time_responses.append(elapsed)


async def start_session(url, session, time_responses):
    try:
        async with session.get(url) as response:
            if response.status // 100 == 2:
                CounterSUCCES()
            elif response.status // 100 in (4, 5):
                CounterFAILED()
    except Exception:
        CounterERROR()


async def main(time_responses, urls, count):
    urls = urls
    tasks = []
    trace_config = aiohttp.TraceConfig()
    trace_config.on_request_start.append(on_request_start)
    trace_config.on_request_end.append(on_request_end)
    timeout = aiohttp.ClientTimeout(total=5)
    for url in urls:
        async with aiohttp.ClientSession(timeout=timeout, trace_configs=[trace_config]) as session:
            for i in range(count):
                task = asyncio.create_task(
                    start_session(url, session, time_responses))
                tasks.append(task)
            await asyncio.gather(*tasks)

        CreateResult.add(url, time_responses)


if __name__ == '__main__':
    time_responses = []  # Массив из времени каждого запроса
    urls, count, output = get_parametrs()
    asyncio.run(main(time_responses, urls, count))
    if output:
        with open(output, 'w') as file:
            file.write(CreateResult.get())
    else:
        print(CreateResult.get())

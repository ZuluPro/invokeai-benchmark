import argparse
from invokeai_benchmark import run
from invokeai_benchmark import __version__

ACTIONS = (
    'text-to-image',
    'clean-images',
)

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--action", default="text_to_image")

    parser.add_argument("-p", "--prompt")
    parser.add_argument("-n", "--negative-prompt", default="")
    parser.add_argument("--width", default=512, type=int)
    parser.add_argument("--height", default=512, type=int)
    parser.add_argument("--seed", default=0, type=int)
    parser.add_argument("--cfg-scale", default=7.5, type=float)
    parser.add_argument("--scheduler", default='euler')
    parser.add_argument("--steps", default=50, type=int)
    parser.add_argument("--fp16", action="store_false", dest="fp32")
    parser.add_argument("--api-url")

    parser.add_argument("--skip-clear-cache", action="store_false", dest="clear_cache")

    parser.add_argument("--verbose", type=int, default=0, help="0: Muted, 1: Info, 2: Verbose")

    opts = vars(parser.parse_args())
    verbose = opts.pop('verbose')
    action = opts.pop('action')

    client = run.Client(
        api_url=opts.pop('api_url'),
        verbose=verbose,
    )

    if action == 'clean-images':
        client.clean_images()
        return

    clear_cache = opts.pop('clear_cache')
    if clear_cache:
        client.clear_cache()
    result = client.full_invoke(**opts)

    result.update(
        version=client.get_version(),
        bench_version=__version__,
    )
    for key, value in result.items():
        print(key, ':', value)


if __name__ == '__main__':
    main()

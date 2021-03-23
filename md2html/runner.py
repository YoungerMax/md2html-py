from md2html.stage import stages


# Run through stages
# Requires the fixed arguments
def run(args):
    # Last return value from last stage
    last_output = None

    # Loop through each registered stage
    for stage in stages:

        # Run each stage and store the return value in
        # last_output for next run
        last_output = stage.run(stage, args, last_output)

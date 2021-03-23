from md2html.stage import stages


# Run through stages
# Requires the fixed arguments
def run(args):
    # Last return value from last stage
    last_output = None

    # For calculating percentages
    complete_amount = 0

    # Loop through each registered stage
    for stage in stages:
        # Update user on the current stage
        print(f"{round(complete_amount / len(stages) * 100)}% | " + stage.get_name(stage))

        # Run each stage and store the return value in
        # last_output for next run
        last_output = stage.run(stage, args, last_output)
        complete_amount += 1

    # Add a final complete message
    backslash = '\\'
    print(f"100% | Complete: file:///{args.output.replace(backslash, '/')}")

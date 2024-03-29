# https://adventofcode.com/2022/day/10


def calc_signal_strengths(cmds):
    reg_x = 1
    cycle = 0
    cycles_to_run = 0
    cmd_idx = 0
    signal_strengths = []
    pending_incr = None
    crt = [[], [], [], [], [], []]  # This could really be built dynamically
    while True:
        # Draw CRT at the start of each cycle
        # Determine the row to draw on (each row is 40 cycles)
        row = cycle // 40
        # Determine whether the cycle's pixel will be lit of dark by checking whether the sprite (reg_x) covers current
        # cycle
        crt[row].append('#' if abs((reg_x + row * 40) - cycle) < 2 else '.')

        # Increment cycle and add value to register (has to be at the start of the cycle)
        cycle += 1
        signal_strengths.append(reg_x)
        # If there's a pending increase to the register, do that and null the pending_incr register
        if pending_incr:
            reg_x += pending_incr
            pending_incr = None
        # Otherwise, handle command
        else:
            try:
                cmd = cmds[cmd_idx].strip()
                # Handle commands and increment total processable cycles based on their type
                if cmd == 'noop':
                    cycles_to_run += 1
                elif cmd.startswith('addx'):
                    cycles_to_run += 2
                    pending_incr = int(cmd.split()[1])
                cmd_idx += 1
            except IndexError:
                pass

        if cmd_idx == len(cmds) and cycle == cycles_to_run:
            break

    return signal_strengths, crt


if __name__ == '__main__':
    with open('inputs/day10') as f:
        cmds = f.readlines()
    signal_strengths, crt = calc_signal_strengths(cmds)

    total_signal_strength = 20 * signal_strengths[19]
    interesting_cycles = (len(signal_strengths) - 20) // 40
    for i in range(1, interesting_cycles + 1):
        total_signal_strength += (i * 40 + 20) * signal_strengths[i * 40 + 19]

    print(total_signal_strength)
    for i in crt:
        print(''.join(i))

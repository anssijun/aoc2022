# https://adventofcode.com/2022/day/7
from collections import defaultdict


if __name__ == '__main__':
    total_size_limit = 70000000
    space_needed = 30000000
    size_limit = 100000
    sizes = defaultdict(int)
    # We know the root is /
    dirs = {'/': {}}
    path = []
    with open('inputs/day7') as f:
        for line in f:
            # parse input line
            if line.startswith('$'):
                # $ denotes a command
                cmd = line[1:].strip()

                if cmd.startswith('cd'):
                    # cd changes path
                    p = cmd.split()[1]
                    # Path is a list so pop to go up
                    if p == '..':
                        path.pop()
                    # And append to go in
                    else:
                        path.append(p)
                elif cmd.startswith('ls'):
                    # Do we even need to do anything with ls?
                    pass
            elif line.startswith('dir'):
                dir_name = line.split()[1]
                current_dir = dirs
                # Get the right subdict by iterating over the path
                for p in path:
                    current_dir = current_dir[p]
                current_dir[dir_name] = current_dir.get(dir_name, {})
            else:
                size, file_name = line.split()
                current_dir = dirs
                current_path = ''
                for p in path:
                    current_dir = current_dir[p]
                    # Keep a track of file sizes in path
                    current_path += f'{p}/'
                    sizes[current_path[1:]] += int(size)
                current_dir[file_name] = int(size)

    # Total space used
    space_used = sizes.get('/')
    smallest_folder_to_delete = space_used
    total_size = 0
    for val in sizes.values():
        # Calculate cumulative sizes for part 1
        if val <= size_limit:
            total_size += val
        # Calculate smallest folder to be deleted for part 2
        if total_size_limit - space_used + val > space_needed and val < smallest_folder_to_delete:
            smallest_folder_to_delete = val

    print('Cumulative size of folders under size limit', total_size)
    print('Smallest folder size to delete', smallest_folder_to_delete)

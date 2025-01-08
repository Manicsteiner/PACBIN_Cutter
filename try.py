import os
import struct
import sys
sys.setrecursionlimit(5000)

import logging

# 设置日志记录
logging.basicConfig(filename='file_processing.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# 定义文件头
TIM2_HEADER = b'\x54\x49\x4D\x32'  # 'TIM2' 的字节表示
LZS_HEADER = b'\x4C\x5A\x53\x00'  # 'LZS' 的字节表示

# 定义裁剪函数
def process_file(input_file):
    # 检查/data文件夹是否存在，不存在则创建
    if not os.path.exists('./data'):
        os.makedirs('./data')

    with open(input_file, 'rb') as f:
        base_offset = 0x002D9800  # 起始偏移量
        file_counter_vis = 0  # 用于计数 vis00000.tm2 文件
        file_counter_il = 0   # 用于计数 il00000.tm2 文件
        offset = base_offset

        while True:
            # 将文件指针移动到当前偏移量
            f.seek(offset)
            
            # 读取文件头判断文件类型
            header = f.read(4)
            
            if header == TIM2_HEADER:
                # 处理 TIM2 类型文件
                start_offset = offset
                # 查找下一个文件头位置
                next_header_pos = find_next_header(f, TIM2_HEADER, LZS_HEADER, start_offset + 16)
                if next_header_pos == -1:
                    # 如果没有找到，表示文件到末尾
                    next_header_pos = os.stat(input_file).st_size
                file_size = next_header_pos - start_offset
                if file_size == 0:
                    offset += 16
                    continue
                file_name = f"vis{file_counter_vis:05d}.tm2"
                output_file = os.path.join('./data', file_name)
                write_file(f, output_file, start_offset, file_size)
                
                # 记录日志
                log_file_info(file_name, start_offset, file_size)
                if file_size > 4 * 1024 * 1024:
                    logging.info(f"{file_name} - Large File Warning")

                file_counter_vis += 1
                offset = next_header_pos

            elif header == LZS_HEADER:
                # 读取接下来的4个字节，检查是否是TIM2类型文件
                f.seek(offset + 9)
                lzs_sub_header = f.read(4)
                if lzs_sub_header == TIM2_HEADER:
                    start_offset = offset
                    next_header_pos = find_next_header(f, TIM2_HEADER, LZS_HEADER, start_offset + 16)
                    if next_header_pos == -1:
                        next_header_pos = os.stat(input_file).st_size
                    file_size = next_header_pos - start_offset
                    if file_size == 0:
                        offset += 16
                        continue
                    file_name = f"il{file_counter_il:05d}.tm2"
                    output_file = os.path.join('./data', file_name)
                    write_file(f, output_file, start_offset, file_size)
                    
                    # 记录日志
                    log_file_info(file_name, start_offset, file_size)
                    if file_size > 4 * 1024 * 1024:
                        logging.info(f"{file_name} - Large File Warning")
                    
                    file_counter_il += 1
                    offset = next_header_pos
                else:
                    # 如果不是TIM2文件，跳过这个LZS文件
                    offset += 16
            elif offset == base_offset:
                start_offset = offset
                next_header_pos = find_next_header(f, TIM2_HEADER, LZS_HEADER, start_offset + 16)
                if next_header_pos == -1:
                    next_header_pos = os.stat(input_file).st_size
                file_size = next_header_pos - start_offset
                file_name = "m0.pss"
                output_file = os.path.join('./data', file_name)
                write_file(f, output_file, start_offset, file_size)
                
                # 记录日志
                log_file_info(file_name, start_offset, file_size)
                if file_size > 4 * 1024 * 1024:
                    logging.info(f"{file_name} - Large File Warning")
                offset = next_header_pos
            else:
                # 如果不是文件头则继续前进
                offset += 16

            # 如果已经到达文件末尾，退出循环
            if offset >= os.stat(input_file).st_size:
                break

# 查找下一个文件头的位置
def find_next_header(file, tim2_header, lzs_header, start_offset):
    file.seek(start_offset)
    content = file.read(1024 * 1024)  # 一次读取 1MB 内容，可以根据实际情况调整
    pos_tim2 = content.find(tim2_header)
    pos_lzs = content.find(lzs_header)
    
    if pos_tim2 == -1 and pos_lzs == -1:
        start_offset += (1024*1024)
        #print("notfind")
        return find_next_header(file, tim2_header, lzs_header, start_offset)  # 没有找到文件头
    
    # 找到的文件头的偏移量
    if pos_tim2 != -1 and (pos_lzs == -1 or pos_tim2 < pos_lzs):
        if pos_tim2 % 16 != 0:
            start_offset += (pos_tim2 // 16 + 1)* 16
            #print("seek " + str(start_offset) + " wrong data " + str(pos_tim2))
            return find_next_header(file, tim2_header, lzs_header, start_offset)
        return start_offset + pos_tim2
    elif pos_lzs != -1:
        if pos_lzs % 16 != 0:
            start_offset += (pos_lzs // 16 + 1)* 16
            #print("seek " + str(start_offset) + " wrong data " + str(pos_lzs))
            return find_next_header(file, tim2_header, lzs_header, start_offset)
        return start_offset + pos_lzs
    return -1

# 写入文件内容
def write_file(file, output_file, start_offset, file_size):
    with open(output_file, 'wb') as out_f:
        file.seek(start_offset)
        out_f.write(file.read(file_size))

# 记录日志信息
def log_file_info(file_name, start_offset, file_size):
    logging.info(f"File: {file_name}, Start Offset: {hex(start_offset)}, Size: {file_size} bytes")

# 主函数，调用过程
if __name__ == "__main__":
    input_file = "PAC.BIN"
    process_file(input_file)

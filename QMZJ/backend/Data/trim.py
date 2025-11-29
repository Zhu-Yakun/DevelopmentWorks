import os

def remove_spaces_in_filenames(target_path):
    """
    递归去除指定路径下所有文件名中的空格
    """
    rename_count = 0  # 记录重命名的文件数量
    error_count = 0   # 记录错误数量
    
    # 遍历目录树
    for root, dirs, files in os.walk(target_path):
        for filename in files:
            # 生成新文件名（去除空格）
            new_filename = filename.replace(" ", "")
            
            if new_filename != filename:
                # 构建旧路径和新路径
                old_path = os.path.join(root, filename)
                new_path = os.path.join(root, new_filename)
                
                try:
                    # 执行重命名操作
                    os.rename(old_path, new_path)
                    print(f"重命名成功: [ {filename} ] -> [ {new_filename} ]")
                    rename_count += 1
                except Exception as e:
                    error_count += 1
                    print(f"错误：无法重命名 [ {filename} ]\n原因: {str(e)}")

    # 最终统计
    print("\n操作完成！")
    print(f"文件处理成功: {rename_count} 个")
    print(f"文件处理失败: {error_count} 个")

if __name__ == "__main__":
    path = './images'
    remove_spaces_in_filenames(path)
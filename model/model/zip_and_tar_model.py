import gzip
import os
import tarfile


def start():
    input_file_path = 'model/model.joblib'
    output_file_path = 'model/model.tar'
    try:
        with tarfile.open(output_file_path, "w") as tar:
            tar.add(input_file_path, arcname=os.path.basename(input_file_path))

        with open(output_file_path, 'rb') as f_in:
            with gzip.open(output_file_path + ".gz", 'wb') as f_out:
                f_out.writelines(f_in)

        os.remove(output_file_path)

        print(f"File '{input_file_path}' successfully gzipped and tarred to '{output_file_path}.gz'")
    except Exception as e:
        print(f"An error occurred: {e}")

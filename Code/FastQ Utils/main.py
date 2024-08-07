import gzip

def fastq_verifier():
    barcode_file = gzip.open("../../Data/input/pbmc3k_fastqs/read-I1_si-ACGCGGAA_lane-001-chunk-001.fastq.gz")
    RA_file = gzip.open("../../Data/input/pbmc3k_fastqs/read-RA_si-ACGCGGAA_lane-001-chunk-001.fastq.gz")
    count = 0


    # Used to track if we read a umi or a transcript
    umi_transcript_flag = True
    RA = ""
    umi = ""
    barcode = ""

    umi = str(next(RA_file).strip()).split(" ")[0]
    next(RA_file)
    next(RA_file)
    next(RA_file)

    try:
        while True:
            if count % 4 == 0:
                barcode = str(next(barcode_file).strip()).split(" ")[0]
            else:
                next(barcode_file)
            if count % 2 == 0:
                ra_or_umi = next(RA_file)
                if umi_transcript_flag:
                    umi_transcript_flag = not umi_transcript_flag
                    RA = str(ra_or_umi.strip()).split(" ")[0]
                else:
                    umi_transcript_flag = not umi_transcript_flag
                    umi = str(ra_or_umi.strip()).split(" ")[0]
                next(RA_file)
            else:
                next(RA_file)
                next(RA_file)

            if count % 4 == 0:
                if not ((barcode == RA) and (umi == RA)):
                    print(f"Broken Lines: {barcode}, {RA}, {umi}")

            count += 1
    except StopIteration:
        print("Parsing Done")


def count_reads():
    #Start at -1 as a offset
    counter = -1
    reads = 0
    with gzip.open("../../Data/input/pbmc3k_fastqs/read-I1_si-ACGCGGAA_lane-001-chunk-001.fastq.gz") as barcode_file:
        for line in barcode_file:
            if not (counter % 4):
                reads += 1
            counter += 1
    return reads


def fastq_entangle():
    #TODO need to write batch of lines instead of single lines since it is very very slow else
    #Splits file by path and then splits file type from name
    original_file_path = "../../Data/input/pbmc3k_fastqs/read-RA_si-ACGCGGAA_lane-001-chunk-001.fastq.gz"
    path_parts = original_file_path.split("/")
    umi_file_path = "/".join(path_parts[:-1]) + "/" + path_parts[-1].split(".")[0] + "_umi.fastq.gz"
    transcript_file_path = "/".join(path_parts[:-1]) + "/" + path_parts[-1].split(".")[0] + "_transcript.fastq.gz"

    #The RA Files contain both the transcript and the umi, this function separates them and put them into different files
    with (gzip.open(original_file_path, mode='rb') as original_file,
         gzip.open(umi_file_path, mode='wb') as umi_file,
         gzip.open(transcript_file_path, mode='wb') as transcript_file):
            counter = 0
            #True => Transcript, False => UMI
            file_flag = True
            for line in original_file:
                if file_flag:
                    transcript_file.write(line)
                else:
                    umi_file.write(line)
                counter += 1
                if not (counter % 4):
                    file_flag = not file_flag


def read_file():
    umi = "../../Data/input/pbmc3k_fastqs/read-RA_si-ACGCGGAA_lane-001-chunk-001_umi.fastq.gz"
    transcript = "../../Data/input/pbmc3k_fastqs/read-RA_si-ACGCGGAA_lane-001-chunk-001_transcript.fastq.gz"
    umi_file = gzip.open(umi)
    transcript_file = gzip.open(transcript)
    to_it = zip(umi_file, transcript_file)
    for lines in to_it:
        print(f"umi {lines[0]}", f"transcript {lines[1]}")

if __name__ == '__main__':
    #fastq_verifier()
    #print(count_reads())
    fastq_entangle()
    #read_file()


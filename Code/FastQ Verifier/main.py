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

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    fastq_verifier()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

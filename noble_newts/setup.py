import tarfile
import requests
import os


def main():
    pwd = os.path.dirname(os.path.realpath(__file__))
    if not os.path.isdir(os.path.join(pwd, 'gsoy-latest')):
        os.mkdir('gsoy-latest')
        os.chdir('gsoy-latest')

        print("Downloading data files...")
        r = requests.get(
            'https://www.ncei.noaa.gov/data/gsoy/archive/gsoy-latest.tar.gz',
            allow_redirects=True
        )
        with open('gsoy-latest.tar.gz', 'wb') as archive:
            archive.write(r.content)
        print("Download complete!")

        print("Extracting data files...")
        with tarfile.open("gsoy-latest.tar.gz") as tar:
            members = tar.getmembers()
            total_members = len(members)
            ten_percent = int(total_members / 10)

            for index, member in enumerate(members):
                if index % ten_percent == 0:
                    print("{}% complete".format(int(index / ten_percent) * 10))
                tar.extract(member)
        print("All files extracted!")


if __name__ == "__main__":
    main()

import json
import pathlib
import mimetypes

from cldfbench import Dataset as BaseDataset


def zip_url(digit):
    return f"https://zenodo.org/records/22796236/files/dogonlanguages_media_{digit}.zip"


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "dogonlanguages"

    def cmd_download(self, args):
        pass

    def cmd_makecldf(self, args):
        args.writer.cldf.add_component('MediaTable', {'name': 'Size', 'datatype': 'integer'}, 'objid_alt', 'fname_alt')
        md5sums = {(r['objid'], r['fname']): r['md5'] for r in self.etc_dir.read_csv('dogonlanguages_md5sums.csv', dicts=True)}
        mds = {}
        for r in self.etc_dir.read_csv('dogonlanguages_files.csv', dicts=True):
            md = json.loads(r['jsondata'])
            for key in ['web', 'original', 'thumbnail']:
                mds[md['objid'], md[key]] = r

        media = {}
        for row in self.etc_dir.read_csv('dogonlanguages_files.tsv', delimiter='\t', dicts=True):
            digit, objid, fname = row['path'].split('/')
            md5 = md5sums[objid, fname]
            md = mds[objid, fname]
            if md5 in media:
                assert not media[md5]['objid_alt']
                media[md5].update(objid_alt=objid, fname_alt=fname)
                continue
            media[md5] = dict(
                ID=md5,
                Name=fname,
                Download_URL=zip_url(digit),
                Path_In_Zip=row['path'],
                Media_Type=mimetypes.guess_type(row['path'])[0] or md.get('mime_type'),
                Size=int(row['size']),
                objid_alt=None,
                fname_alt=None,
            )
        for d in media.values():
            args.writer.objects['MediaTable'].append(d)


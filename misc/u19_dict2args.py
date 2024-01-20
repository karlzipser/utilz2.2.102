from utilz2.misc.u13_printing import *
import argparse


def getparser( **argdic ):
    if interactive():
        return kws2class(**argdic)
    parser = argparse.ArgumentParser(description='Argument Parser')
    for k in argdic:
        if len(k)>1:
            s='--'
        else:
            s='-'
        parser.add_argument(s+k,type=type(argdic[k]),default=argdic[k])
    return parser.parse_args()



if __name__ == '__main__':

    args=getparser(
        png_with_mask_dir_path= opjD('aug-in/rgb4-geometry/images'),
        mask_and_rgb_dst=       opjh('Pytorch-MADFexamples/places'),
        result_dir=             opjD('inpainted'),
        max_n=                  0,
        kernel_size=            5,
    )
    kprint( args.__dict__)



#EOF

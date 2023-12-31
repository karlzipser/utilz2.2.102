def batch(category_name='rhib-wake-hard-masks'):


    category_name='rhib-wake-hard-masks'
    src_rgb_path = opjD('itc-2023-unified/boats/processed/rgb-hard')
    mask_path = opjD('itc-2023-unified/boats/processed/rhib-wake-hard-masks')
    mkdirp( mask_path )

    fs = sggo(src_rgb_path,'*.*')
    ms = sggo(mask_path,'*.*')

    md = {}
    for m in ms:
        md[fname(m)] = m


    print(len(fs),'files to process')
    for f in fs:
        if fname(f) in md:
            cr('***',fname(f),'already processed.')
            continue
        print(f)

        l = [
                    'python3',
                    'k3/misc/ger/utils/draw_segmentation.py',
                    f,
                    opj(mask_path,fname(f)),
                    category_name,
                    '512',
                ]
        cg(' '.join(l))
        subprocess.run(
            l,
            check=True
        )

    print('Done.')
    os_system('say done')
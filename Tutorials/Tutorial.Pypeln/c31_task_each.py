import pypeln as pl

def process_image(image_path):
    image = load_image(image_path)
    image = transform_image(image)
    save_image(image_path, image)

def main():
    files_paths = get_file_paths()
    stage = pl.task.each(process_image, file_paths, workers=4)
    pl.task.run(stage)

if __name__ == '__main__':
    main()

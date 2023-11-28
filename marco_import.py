import os
import tensorflow as tf

feature_description = {
    'image/height': tf.io.FixedLenFeature([], tf.int64),
    'image/width': tf.io.FixedLenFeature([], tf.int64),
    'image/colorspace': tf.io.FixedLenFeature([], tf.string),
    'image/channels': tf.io.FixedLenFeature([], tf.int64),
    'image/class/label': tf.io.FixedLenFeature([], tf.int64),
    'image/class/raw': tf.io.FixedLenFeature([], tf.int64),
    'image/class/source': tf.io.FixedLenFeature([], tf.int64),
    'image/class/text': tf.io.FixedLenFeature([], tf.string),
    'image/format': tf.io.FixedLenFeature([], tf.string),
    'image/filename': tf.io.FixedLenFeature([], tf.string),
    'image/id': tf.io.FixedLenFeature([], tf.int64),
    'image/encoded': tf.io.FixedLenFeature([], tf.string),
}

def save_images_by_label(example, output_directory):
    """
    saves the TFRecord contents as a jpg, in folders for each class:
    0 - Clear
    1 - Crystals
    2 - Other
    3 - Precipitate
    """
    example = tf.io.parse_single_example(example, feature_description)
    image = tf.image.decode_jpeg(example['image/encoded'], channels=3)  # Decode JPEG image
    label = example['image/class/label'].numpy()  # Get label value as numpy int

    # Create a folder for each label if it doesn't exist
    label_dir = os.path.join(output_directory, str(label))
    if not os.path.exists(label_dir):
        os.makedirs(label_dir)

    # Save the image to the respective label folder
    image_filename = example['image/filename'].numpy().decode('utf-8')  # Get filename as string
    image_path = os.path.join(label_dir, image_filename)
    tf.io.write_file(image_path, tf.image.encode_jpeg(image))


tfrecord_directory = 'MARCO_TFRecords'
tfrecord_files = os.listdir(tfrecord_directory)

for file_name in tfrecord_files:

    # Read TFRecord file
    tfrecord_file = os.path.join(tfrecord_directory, file_name)
    output_directory = 'MARCO_IMAGES'
    dataset = tf.data.TFRecordDataset(tfrecord_file)

    # Process and save images by label
    for record in dataset:
        save_images_by_label(record, output_directory)
from keras.callbacks import TensorBoard, ModelCheckpoint, EarlyStopping
from seg_model import get_unet, UNetEvaluator
from config import *
from generators import get_seg_batch

def seg_train():
    print('start seg_train')
    model = get_unet()
    model.summary()

    print("TRAIN_ROUND {}".format(SEG_NET_TRAIN_ROUND))
    tensorboard = TensorBoard(log_dir=SEG_LOG_DIR, histogram_freq=0, write_grads=False, write_graph=False)
    checkpoint = ModelCheckpoint(filepath=SEG_LOG_FILE_PATH, monitor='val_loss', verbose=1, save_best_only=True)
    early_stopping = EarlyStopping(monitor='val_loss', patience=TRAIN_SEG_EARLY_STOPPING_PATIENCE, verbose=1)
    evaluator = UNetEvaluator()
    model.fit_generator(get_seg_batch(TRAIN_SEG_TRAIN_BATCH_SIZE), steps_per_epoch=TRAIN_SEG_STEPS_PER_EPOCH,
                        validation_data=get_seg_batch(TRAIN_SEG_VALID_BATCH_SIZE), validation_steps=TRAIN_SEG_VALID_STEPS,
                        epochs=TRAIN_SEG_EPOCHS, verbose=1,
                        callbacks=[tensorboard, checkpoint, early_stopping, evaluator])

if __name__ == '__main__':
    seg_train()
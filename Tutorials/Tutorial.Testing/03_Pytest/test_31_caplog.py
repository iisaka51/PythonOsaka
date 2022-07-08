import logging

LOGGER = logging.getLogger(__name__)

def myfunc():
    LOGGER.info('LOGLevel info')
    LOGGER.warning('LOGLevel warning')
    LOGGER.error('LOGLevel error')
    LOGGER.critical('LOGLevel critical')

class TestCapLog:
    def test_caplog1(self, caplog):
        myfunc()

        assert (__name__, logging.INFO, "LOGLevel info") \
                not in caplog.record_tuples, \
                "ログレベルはWARNINGがデフォルトなので、INFOは出力されない"
        assert (__name__, logging.WARNING, "LOGLevel warning") \
                in caplog.record_tuples
        assert (__name__, logging.ERROR, "LOGLevel error") \
                in caplog.record_tuples

        caplog.set_level(logging.INFO)
        myfunc()

        assert (__name__, logging.INFO, "LOGLevel info") \
               in caplog.record_tuples, \
               "ログレベルをINFOにしたので、このログは出力される"

    def test_caplog2(self, caplog):
        # test_caplog1 で設定したログレベルはテスト終了時にリセットされている
        myfunc()

        assert (__name__, logging.INFO, "LOGLevel info") \
                not in caplog.record_tuples, \
                "ログレベルはWARNINGがデフォルトなので、INFOは出力されない"
        assert (__name__, logging.WARNING, "LOGLevel warning") \
                in caplog.record_tuples
        assert (__name__, logging.ERROR, "LOGLevel error") \
                in caplog.record_tuples

        with caplog.at_level(logging.INFO):
            myfunc()

        assert (__name__, logging.INFO, "LOGLevel info") \
               in caplog.record_tuples, \
               "ログレベルをINFOにしたので、このログは出力される"


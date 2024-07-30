import logging
import threading
import time

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s (%(threadName)-2s) %(message)s')


def consumer(cond, buffer):
    """Wait for the condition and consume from the buffer"""
    logging.debug('Iniciando hilo consumidor')
    with cond:
        while not buffer:
            logging.debug('El buffer está vacío. Esperando producción.')
            cond.wait()
        item = buffer.pop(0)
        logging.debug('Consumiendo el recurso: %s', item)


def producer(cond, buffer):
    """Produce a resource and notify the consumer"""
    
    logging.debug('Iniciando el hilo productor')
    with cond:
        for i in range(10):
            if len(buffer) >= 10:
                logging.debug('El buffer está lleno. Esperando consumo.')
                cond.wait()
            item = f'Recurso {i}'
            buffer.append(item)
            logging.debug('Produciendo el recurso: %s', item)
        cond.notify_all()


condition = threading.Condition()
buffer = []

c1 = threading.Thread(name='c1', target=consumer, args=(condition, buffer))
c2 = threading.Thread(name='c2', target=consumer, args=(condition, buffer))
p = threading.Thread(name='p', target=producer, args=(condition, buffer))

c1.start()
time.sleep(2)
c2.start()
time.sleep(2)
p.start()
import os
from utils import toBytes
from cffi_utils.sowrapper import get_lib_ffi_shared
from pkg_resources import resource_filename


c_hdr = '''
void poly1305_auth(unsigned char mac[16],
                   const unsigned char *m,
                   size_t bytes,
                   const unsigned char key[32]);

int poly1305_verify(const unsigned char mac1[16],
                    const unsigned char mac2[16]);

int poly1305_power_on_self_test(void);
'''


libpath = resource_filename('poly1305_donna', 'libpoly1305donna.so')
(ffi, lib) = get_lib_ffi_shared(libpath=libpath, c_hdr=c_hdr)


class Poly1305(object):
    @classmethod
    def self_test(cls):
        '''
        Returns-->boolean
        '''
        return (lib.poly1305_power_on_self_test() == 1)

    @classmethod
    def get_key(cls, random_fn=None):
        '''
        random_fn-->callable: takes one int param: number of random bytes
                    Preferably leave unset; os.urandom() will be used
        Returns-->bytes: Secure key
        '''
        if random_fn is None:
            random_fn = os.urandom
        kr = ffi.new('unsigned char[32]', random_fn(32))
        return ffi.get_bytes(kr)

    @classmethod
    def authenticate(cls, kr, msg, random_fn=None):
        '''
        kr-->bytes: Secure key - returned by get_key()
        msg-->str or bytes: Message to be authenticated
        random_fn-->callable: takes one int param: number of random bytes
                    Preferably leave unset; os.urandom() will be used
        Returns-->bytes: auth
        '''
        if random_fn is None:
            random_fn = os.urandom
        auth = ffi.new('unsigned char[16]')
        msg = toBytes(msg)

        lib.poly1305_auth(auth, msg, len(msg), kr)
        return ffi.get_bytes(auth)

    @classmethod
    def verify(cls, auth, kr, msg, random_fn=None):
        '''
        auth-->bytes
        kr-->bytes: Secure key - returned by get_key()
        msg-->str or bytes: Message to be authenticated
        Returns-->boolean
        '''
        (auth, kr, msg) = (toBytes(auth), toBytes(kr), toBytes(msg))
        auth2 = cls.authenticate(kr, msg, random_fn=random_fn)
        return (lib.poly1305_verify(auth, auth2) == 1)


if __name__ == '__main__':
    p = Poly1305
    print('Power-On Self Test result: ' + str(p.self_test()))
    msg = 'Hello world'
    print('\nTest class methods - authenticate, verify')
    kr = p.get_key()
    auth = p.authenticate(kr, msg)

    bad_kr = p.get_key()
    bad_msg = msg + '1'
    bad_auth = p.authenticate(kr, bad_msg)

    print('Good: %s\nBad auth: %s\nBad kr: %s\nBad msg: %s' % (
        str(p.verify(auth, kr, msg)),
        str(p.verify(bad_auth, kr, msg)),
        str(p.verify(auth, bad_kr, msg)),
        str(p.verify(auth, kr, bad_msg))
    ))

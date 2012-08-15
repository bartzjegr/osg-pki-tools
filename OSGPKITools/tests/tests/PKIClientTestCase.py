"""PKIClientTestCase: OSG PKI Command line client test case base class"""

import os
import os.path
import scripttest  # pip install scripttest
import unittest

class PKIClientTestCase(unittest.TestCase):
    """OSG PKI CLI TestCase bass class"""

    # Path to user certificate and private key to use for authentication
    user_cert_path = None
    user_key_path = None

    # Information to provide with requests
    email = "osg-pki-cli-test@example.com"
    name = "OSG PKI CLI Test Suite"
    phone = "555-555-5555"

    # Domain to use with host certificate requests
    domain = "bw.iu.edu"  # XXX: This is specific to Von

    # Private key pass phrase
    pass_phrase = None

    # Openssl binary
    openssl = "openssl"

    # Where the scripts are relative to the tests/ directory
    scripts_path = os.path.abspath("..")

    @classmethod
    def get_test_env(cls):
        """Return a scripttest.TestFileEnvironment instance"""
        # Make sure our source path is in PYTHONPATH so we can
        # find imports
        env = dict(os.environ)
        if env.has_key("PYTHONPATH"):
            env["PYTHONPATH"] += ":" + cls.scripts_path
        else:
            env["PYTHONPATH"] = cls.scripts_path
        env = scripttest.TestFileEnvironment("./test-output",
                                             environ=env,
                                             template_path=cls.scripts_path)
        # Copy in configuration file
        env.writefile("OSGPKIClients.ini", frompath="OSGPKIClients.ini")
        return env

    @classmethod
    def run_cmd(cls, env, *args):
        """Run given command.

        This is a wrapper around env.run() that won't throw an exception
        on error so we can handle errors in the test framework.

        Returns scriptTest.ProcResult instance from TestFileEnvironment.run()"""
        # Python 2.4 requires kwargs to be defined in variable and then
        # expanded in call to env.run instead of being supplied as keywords
        kwargs = {
            # Don't raise exception on error
            "expect_error" : True,
            "expect_stderr" : True,
            "quiet" : True,
            }
        result = env.run(*args, **kwargs)
        return result

    @classmethod
    def run_script(cls, env, script, *args):
        """Run script with given arguments.

        Returns scriptTest.ProcResult instance from TestFileEnvironment.run()"""
        # Python 2.4 requires kwargs to be defined in variable and then
        # expanded in call to env.run instead of being supplied as keywords
        kwargs = {
            # Don't raise exception on error
            "expect_error" : True,
            "expect_stderr" : True,
            "quiet" : True,
            }
        result = env.run("python",  # In case script is not executable
                         os.path.join(cls.scripts_path, script),
                         *args, **kwargs)
        return result

    def run_python(cls, code, *args):
        """Run given python code

        Returns scriptTest.ProcResult instance from TestFileEnvironment.run()"""
        env = cls.get_test_env()
        # Python 2.4 requires kwargs to be defined in variable and then
        # expanded in call to env.run instead of being supplied as keywords
        kwargs = {
            # Don't raise exception on error
            "expect_error" : True,
            "expect_stderr" : True,
            "quiet" : True,
            }
        result = env.run("env")
        result = env.run("python", "-c", code, *args, **kwargs)
        return result

    @classmethod
    def run_error_msg(cls, result):
        """Return an error message from a result"""
        return "Return code: %d\n" % result.returncode \
            + result.stdout + result.stderr

    @classmethod
    def set_cert_path(cls, path):
        """Set path to use for user certificate"""
        cls.user_cert_path = path

    @classmethod
    def get_cert_path(cls):
        """Return path to user certificate to use for authentication

        Search order is:
           Path specified by user on commandline
           ./test-cert.pem"""
        if cls.user_cert_path:
            return cls.user_cert_path
        return os.path.expanduser("./test-cert.pem")

    @classmethod
    def set_key_path(cls, path):
        """Set path to use for user private key"""
        cls.user_key_path = path

    @classmethod
    def get_key_path(cls):
        """Return path to user private key to use for authentication

        Search order is:
           Path specified by user on commandline
           ./test-key.pem"""
        if cls.user_key_path:
            return cls.user_key_path
        return os.path.expanduser("./test-key.pem")

    @classmethod
    def set_scripts_path(cls, path):
        """Set the path to where the scripts are"""
        cls.scripts_path = os.path.abspath(path)

    @classmethod
    def get_scripts_path(cls):
        """Get the path to where the scripts are"""
        return cls.scripts_path

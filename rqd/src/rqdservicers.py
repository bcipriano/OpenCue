
import logging as log

import rqd_pb2
import rqd_pb2_grpc


def responseManager(responseType):
    """
    Decorator that tries to run the wrapped function. If any exception is thrown, use the error status code.
    :param responseType: Response object type to return.
    :return: Response object instance.
    """
    def decorator(func):
        def attemptor(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except Exception, e:
                return responseType(1, 'Failed to run request: {}'.format(e))
            return responseType(0, 'Success')
        return attemptor
    return decorator


class RqdStaticServicer(rqd_pb2_grpc.RqdInterfaceServicer):
    """Service interface for RqdStatic gRPC definition"""

    def __init__(self, rqCore):
        self.rqCore = rqCore

    @responseManager(rqd_pb2.RqdStaticLaunchFrameResponse)
    def launchFrame(self, request, context):
        """RPC call that launches the given frame"""
        log.info("Request received: launchFrame")
        self.rqCore.launchFrame(request)

    def reportStatus(self, request, context):
        """RPC call that returns reportStatus"""
        log.info("Request received: reportStatus")
        return rqd_pb2.RqdStaticReportStatusResponse(self.rqCore.reportStatus())

    def getRunningFrameStatus(self, request, context):
        """RPC call to return the frame info for the given frame id"""
        log.info("Request received: getRunningFrameStatus")
        frame = self.rqCore.getRunningFrame(request.frameId)
        return rqd_pb2.RqdStaticGetRunningFrameStatusResponse(frame.runningFrameInfo())

    @responseManager(rqd_pb2.RqdStaticKillRunningFrameResponse)
    def killRunningFrame(self, request, context):
        """RPC call that kills the running frame with the given id"""
        log.info("Request received: killRunningFrame")
        frame = self.rqCore.getRunningFrame(request.frameId)
        frame.kill()

    @responseManager(rqd_pb2.RqdStaticShutdownNowResponse)
    def shutdownRqdNow(self, request, context):
        """RPC call that kills all running frames and shuts down rqd"""
        log.info("Request recieved: shutdownRqdNow")
        self.rqCore.shutdownRqdNow()

    @responseManager(rqd_pb2.RqdStaticShutdownIdleResponse)
    def shutdownRqdIdle(self, request, context):
        """RPC call that locks all cores and shuts down rqd when it is idle.
           unlockAll will abort the request."""
        log.info("Request recieved: shutdownRqdIdle")
        self.rqCore.shutdownRqdIdle()

    @responseManager(rqd_pb2.RqdStaticRestartNowResponse)
    def restartRqdNow(self, request, context):
        """RPC call that kills all running frames and restarts rqd"""
        log.info("Request recieved: restartRqdNow")
        self.rqCore.restartRqdNow()

    @responseManager(rqd_pb2.RqdStaticRestartIdleResponse)
    def restartRqdIdle(self, request, context):
        """RPC call that that locks all cores and restarts rqd when idle.
           unlockAll will abort the request."""
        log.info("Request recieved: restartRqdIdle")
        self.rqCore.restartRqdIdle()

    @responseManager(rqd_pb2.RqdStaticRebootNowResponse)
    def rebootNow(self, request, context):
        """RPC call that kills all running frames and reboots the host."""
        log.info("Request recieved: rebootNow")
        self.rqCore.rebootNow()

    @responseManager(rqd_pb2.RqdStaticRebootIdleResponse)
    def rebootIdle(self, request, context):
        """RPC call that that locks all cores and reboots the host when idle.
           unlockAll will abort the request."""
        log.info("Request recieved: rebootIdle")
        self.rqCore.rebootIdle()

    @responseManager(rqd_pb2.RqdStaticNimbyOnResponse)
    def nimbyOn(self, request, context):
        """RPC call that activates nimby"""
        log.info("Request recieved: nimbyOn")
        self.rqCore.nimbyOn()

    @responseManager(rqd_pb2.RqdStaticNimbyOffResponse)
    def nimbyOff(self, request, context):
        """RPC call that deactivates nimby"""
        log.info("Request recieved: nimbyOff")
        self.rqCore.nimbyOff()

    @responseManager(rqd_pb2.RqdStaticLockResponse)
    def lock(self, request, context):
        """RPC call that locks a specific number of cores"""
        log.info("Request recieved: lock %d" % request.cores)
        self.rqCore.lock(request.cores)

    @responseManager(rqd_pb2.RqdStaticLockAllResponse)
    def lockAll(self, request, context):
        """RPC call that locks all cores"""
        log.info("Request recieved: lockAll")
        self.rqCore.lockAll()

    @responseManager(rqd_pb2.RqdStaticUnlockResponse)
    def unlock(self, request, context):
        """RPC call that unlocks a specific number of cores"""
        log.info("Request recieved: unlock %d" % request.cores)
        self.rqCore.unlock(request.cores)

    @responseManager(rqd_pb2.RqdStaticUnlockAllResponse)
    def unlockAll(self, request, context):
        """RPC call that unlocks all cores"""
        log.info("Request recieved: unlockAll")
        self.rqCore.unlockAll()
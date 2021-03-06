#/************************************************************************************************************************
# Copyright (c) 2016, Imagination Technologies Limited and/or its affiliated group companies.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#     1. Redistributions of source code must retain the above copyright notice, this list of conditions and the
#        following disclaimer.
#     2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
#        following disclaimer in the documentation and/or other materials provided with the distribution.
#     3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
#        products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#************************************************************************************************************************/

from framework.awa_enums import AwaError
from framework.awa_exceptions import AwaUnexpectedErrorException
from operation_assertions_common import CheckForException
import write_operation_assertions
from framework.test_assertions import WriteAssertion

def CheckForSuccess(testCase, assertion):
    session = testCase.topology.gatewayServers[0]._session
    observation = testCase.topology.gatewayServers[0].CreateObservation(testCase.client_id, assertion.path)

    testCase.topology.gatewayServers[0].Observe(session, observation, testCase.client_id)

    if assertion.writeWithDaemon:
        write_operation_assertions.CheckForSuccess(testCase, WriteAssertion(None, assertion.path, assertion.resourceType, assertion.expectedValue, writeMode=assertion.writeMode))

    testCase.topology.gatewayServers[0].WaitForNotification(session, assertion.path)

    notifyValue = testCase.topology.gatewayServers[0].GetNotifyResponse(assertion.path)
    testCase.assertEqual(notifyValue, assertion.expectedValue)

    testCase.topology.gatewayServers[0].CancelObservation(session, observation, testCase.client_id)

    testCase.topology.gatewayServers[0].FreeObservation(observation)

def CheckForPathNotFound(testCase, assertion):
    CheckForException(testCase, CheckForSuccess, assertion, AwaUnexpectedErrorException, AwaError.Response, AwaError.PathNotFound)

def CheckForTypeMismatch(testCase, assertion):
    CheckForException(testCase, CheckForSuccess, assertion, AwaUnexpectedErrorException, AwaError.Response, AwaError.TypeMismatch)

def CheckForCannotCreate(testCase, assertion):
    CheckForException(testCase, CheckForSuccess, assertion, AwaUnexpectedErrorException, AwaError.Response, AwaError.CannotCreate)

#################################################################################
#                                                                               #
# autobuffer                                                                    #
#                                                                               #
# A simple and fast automatic double buffer class for 1-D data streaming        #
#                                                                               #
# (C) Copyright 2021, João Dias Carrilho                                        #
#                                                                               #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS       #
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,   #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE   #
# AUTHOR(S) OR COPYRIGHT HOLDER(S) BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER    #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, #
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE #
# SOFTWARE.                                                                     #
#                                                                               #
#################################################################################

from numpy import ravel, asarray

class autoBuffer:
        def __init__(self):
                self.buffer = [[],[]]
                self.currentHalf2write = 0
                self.currentHalf2read = 1
                
        def enque(self, item):
                self.buffer[self.currentHalf2write].append(item)

        def deque(self):
                self.currentHalf2read = self.currentHalf2write
                self.currentHalf2write = 1-self.currentHalf2write # Toggle it!
                #flat_list = [item for row in self.buffer[self.currentHalf2read] for item in row]
                flat_list = asarray(self.buffer[self.currentHalf2read]).ravel()
                self.buffer[self.currentHalf2read] *= 0 # clear the just read buffer half
                return flat_list

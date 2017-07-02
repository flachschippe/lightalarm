#!/usr/bin/python
import smbus
from time import sleep


class Lightsensor:
    CtrlReg = 0x80;
    TimingReg = 0x81;
    IdReg = 0x8a;
    Data0Reg = 0x8c;
    Data1Reg = 0x8e;


    GAIN = 0;
    Manual = 0;
    INTEG = 0;
    Address = 0x39;
    Busnumber = 1;
    I2c = None;
    Id = 0;
    def __init__(self):
        self.I2c = smbus.SMBus(self.Busnumber)
        print ":" + str(self.readByte(0x81))
        self.writeByte(self.CtrlReg, 0x03);
        
        self.Id = self.readByte(self.IdReg);
        self.readTimingReg();
        

    def writeByte(self, Address, Data):
        self.I2c.write_byte_data(self.Address, Address, Data)

    
    def readByte(self, Address):
        return self.I2c.read_byte_data(self.Address, Address)        
        
    def readWord(self, Address):
        return self.I2c.read_word_data(self.Address | 0x20, Address)        

    def getData0(self):
        return self.readWord(self.Data0Reg); 

    def getData1(self):
        return self.readWord(self.Data1Reg); 

    def setGain(self, Val):
        timingRegVal =  self.readByte(self.TimingReg)
        if (Val != 0):
            self.writeByte(self.TimingReg, timingRegVal | 0x10)
        else:
            self.writeByte(self.TimingReg, timingRegVal & ~0x10)
        self.readTimingReg();
        
    def readTimingReg(self):
        timingRegVal =  self.readByte(self.TimingReg)
        self.GAIN = (timingRegVal & 0x10) >> 4;
        self.Manual = (timingRegVal & 0x08) >> 3;
        self.INTEG = (timingRegVal & 0x02);
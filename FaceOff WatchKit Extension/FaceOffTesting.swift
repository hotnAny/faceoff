//
//  FaceOffTesting.swift
//  FaceOff WatchKit Extension
//
//  Created by Xiang 'Anthony' Chen on 3/25/20.
//  Copyright © 2020 Xiang 'Anthony' Chen. All rights reserved.
//

import WatchKit
import Foundation
import CoreMotion
import HealthKit
import CoreML

class FaceOffTesting: WKInterfaceController {
    
    // overall
    var readyForInferencing :Bool = false
    var timer :Timer? = nil
    
    // sensor data
    let SAMPLINGRATE :Double = FaceOffConfig.SAMPLINGRATE
    let INFERENCERATE :Double = 4
    let motionManager = CMMotionManager()
    var bufAccel :[Float] = []
    var tsAccel :[Int64] = []
    var ptrAccel = 0
    
    // timing
    let TIMEWINDOW = FaceOffConfig.TIMEWINDOW
    
    // ml
//    let nnModel = nnclf()
    
    // user testing
    let ISDRYRUN = false
    var isTesting = false
    var timeLastAction :Int64 = -1
    var timeLastNonActionMark :Int64 = -1
    let windowDataCollection = 2 * FaceOffConfig.TIMEWINDOW
    var countActions = 0
    @IBOutlet weak var swTesting: WKInterfaceSwitch!
    @IBOutlet weak var lbInstr: WKInterfaceLabel!
    @IBOutlet weak var btnCfmInstr: WKInterfaceButton!
    var cntdownAction = -1
    var clsAction = ""
    var touchOngoing = false
    let prepTimeForTouch = 4000
    var intervalNextTouch = 60  // seconds
    
    // other ui
    @IBOutlet weak var lbWarning: WKInterfaceLabel!
    var alphaWarning :CGFloat = 0
    
    override func awake(withContext context: Any?) {
        super.awake(withContext: context)
        
        print("debugger is working!")
        
        motionManager.accelerometerUpdateInterval = 1 / SAMPLINGRATE //0.01s
    }
    
    override func willActivate() {
        super.willActivate()
        
        if !motionManager.isAccelerometerAvailable {
            print("accelerometer unavailable!")
        }
        
        if !ISDRYRUN && !motionManager.isAccelerometerAvailable && !motionManager.isGyroAvailable {
            return
        }
        
        intervalNextTouch -= Int((windowDataCollection + prepTimeForTouch) / 1000)
        
        print(intervalNextTouch)
        
        timer = Timer.scheduledTimer(withTimeInterval: 1 / INFERENCERATE, repeats: true) { timer in
            
            // initial data gathering for readiness
            if !self.ISDRYRUN && !self.readyForInferencing {
                return
            }
            
            if !self.isTesting {
                return
            }
            
            //
            // look backwards to gather sensor data in the last TIMEWINDOW
            // ISSUE: sometimes sensor rate is low due to energy saving and there aren't enough data points
            //
            var bufAccel :[Float] = []
            if !self.ISDRYRUN {
                var idx = self.ptrAccel
                let tsCurrent = self.tsAccel[idx/3]
                while(bufAccel.count < self.bufAccel.count) {
                    bufAccel.append(self.bufAccel[idx])
                    bufAccel.append(self.bufAccel[idx+1])
                    bufAccel.append(self.bufAccel[idx+2])
                    
                    idx = (idx + self.bufAccel.count - 3) % self.bufAccel.count
                    let ts = self.tsAccel[idx/3]
                    if tsCurrent - ts > self.TIMEWINDOW {
                        break
                    }
                }
            }
            
            
            //
            // collect data labeled as face touching
            //
            let timeSinceLastAction = FaceOff.getCurrentMillis()-self.timeLastAction
            if timeSinceLastAction < self.windowDataCollection {
                print(FaceOff.stringize(bufAccel) + "Touching")
                self.touchOngoing = true
                
            } else if self.cntdownAction == -1 {
                
                // if a face touching just took place, update to the next face touching part
                if self.touchOngoing {
                    Timer.scheduledTimer(withTimeInterval: TimeInterval(self.intervalNextTouch), repeats: false) { timer in
                        self.clsAction = self.getNextAction()
                        self.lbInstr.setText(self.clsAction)
                        self.btnCfmInstr.setTitle("Got it!")
                        for _ in 1...6 {
                            WKInterfaceDevice.current().play(.notification)
                        }
                    }
                    self.touchOngoing = false
                }
                
                // collect data labeled as non face touching
                print(FaceOff.stringize(bufAccel) + "No Touching")
                self.timeLastNonActionMark = FaceOff.getCurrentMillis()
                
            }
            
            //
            // count down for a face touching action
            //
            let n = self.prepTimeForTouch / (1000 / Int(self.INFERENCERATE))
            if self.cntdownAction == n {
                self.countActions += 1
                print("Action #" + String(self.countActions) + " do something")
                // 2nd vibration
                for _ in 1...32 {
                    WKInterfaceDevice.current().play(.notification)
                }
                self.timeLastAction = FaceOff.getCurrentMillis()
                self.cntdownAction = -1
            } else if self.cntdownAction >= 0 {
                self.cntdownAction += 1
            }
        }
        
        let handler:CMAccelerometerHandler = {(data: CMAccelerometerData?, error: Error?) -> Void in
            
            let scaledup = 1.25 // collect a little more than the TIMEWINDOW needs
            let interval = 1000 / self.SAMPLINGRATE
            
            // initially, filling up the buffer
            if self.bufAccel.count < (Int)((Double)(3 * self.TIMEWINDOW) * scaledup / interval) {
                self.bufAccel.append((Float)(data!.acceleration.x))
                self.bufAccel.append((Float)(data!.acceleration.y))
                self.bufAccel.append((Float)(data!.acceleration.z))
                self.tsAccel.append(FaceOff.getCurrentMillis())
                self.ptrAccel = self.bufAccel.count
            }
                // when the buffer is full, overwrite the oldest values
            else {
                self.readyForInferencing = true
                let idx = (self.ptrAccel + 3) % self.bufAccel.count
                self.bufAccel[idx] = (Float)(data!.acceleration.x)
                self.bufAccel[idx + 1] = (Float)(data!.acceleration.y)
                self.bufAccel[idx + 2] = (Float)(data!.acceleration.z)
                self.tsAccel[idx / 3] = FaceOff.getCurrentMillis()
                self.ptrAccel = idx
            }
        }
        
        // start accelerometer
        motionManager.startAccelerometerUpdates(to: OperationQueue.current!, withHandler: handler)
    }
    
    override func didDeactivate() {
        super.didDeactivate()
        if !FaceOffConfig.ALWAYSON {
            motionManager.stopAccelerometerUpdates()
            timer?.invalidate()
        }
        print("deactivated")
    }
    
    @IBAction func testingToggled(_ value: Bool) {
        self.isTesting = value
        self.lbInstr.setHidden(!value)
        self.btnCfmInstr.setHidden(!value)
        if value {
            lbInstr.setText(self.getNextAction())
        }
    }
    
    @IBAction func confirmIntrr() {
        self.cntdownAction = 0
        print("counting down ...")
        self.btnCfmInstr.setTitle("Wait ...")
    }
    
    func getNextAction()->String{
        var clsAction = self.clsAction
        while clsAction == self.clsAction {
            clsAction = FaceOffConfig.UPARTSTOUCHED[Int.random(in: 0 ... FaceOffConfig.UPARTSTOUCHED.count-1)]
        }
        
        return clsAction
    }    
}

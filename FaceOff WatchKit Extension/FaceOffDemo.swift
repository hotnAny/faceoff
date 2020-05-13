//
//  FaceOffDemo.swift
//  FaceOff WatchKit Extension
//
//  Created by Xiang 'Anthony' Chen on 5/12/20.
//  Copyright © 2020 Xiang 'Anthony' Chen. All rights reserved.
//

import WatchKit
import Foundation
import CoreMotion
import HealthKit

class FaceOffDemo: WKInterfaceController {
    
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
        
        if !motionManager.isAccelerometerAvailable && !motionManager.isGyroAvailable {
            return
        }
        
        
        timer = Timer.scheduledTimer(withTimeInterval: 1 / INFERENCERATE, repeats: true) { timer in
            
            // initial data gathering for readiness
            if !self.readyForInferencing {
                return
            }
            
            //
            var bufAccel :[Float] = []
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
            
            //
            //  making inference
            //
            self.makeInference(bufAccel: bufAccel)
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
        // This method is called when watch view controller is no longer visible
        super.didDeactivate()
    }
    
    func makeInference(bufAccel: [Float]) {
        let data = preproc(bufAccel)
        if data.count == NFEATURES {
            
            if classifyByRule(data){
                print("Don't touch your face!")
                for _ in 1...12 {
                    WKInterfaceDevice.current().play(.notification)
                }
                self.lbWarning.setAlpha(1.0)
                self.alphaWarning = 1.0
                self.bufAccel = []
                self.readyForInferencing = false
            } else {
                self.alphaWarning *= 0.95
                self.lbWarning.setAlpha(self.alphaWarning)
            }
        }
        
    }
    
}

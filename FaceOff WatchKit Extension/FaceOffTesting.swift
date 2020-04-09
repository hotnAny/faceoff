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
    @IBOutlet weak var timerStub: WKInterfaceTimer!
    
    // sensor data
    let SAMPLINGRATE :Double = FaceOffConfig.SAMPLINGRATE
    let INFERENCERATE :Double = FaceOffConfig.INFERENCERATE
    let motionManager = CMMotionManager()
    var bufAccel :[Float] = []
    var tsAccel :[Int64] = []
    var ptrAccel = 0
    
    // timing
    let TIMEWINDOW = FaceOffConfig.TIMEWINDOW
    
    // ml
    let nnModel = nnclf()
    
    @IBOutlet weak var lbWarning: WKInterfaceLabel!
    var alphaWarning :CGFloat = 0
    
    override func awake(withContext context: Any?) {
        super.awake(withContext: context)
        
        print("debugger is working!")
        
        motionManager.accelerometerUpdateInterval = 1 / SAMPLINGRATE //0.01s
        //        motionManager.gyroUpdateInterval = 1
    }
    
    override func willActivate() {
        super.willActivate()
        
        if !motionManager.isAccelerometerAvailable {
            print("accelerometer unavailable!")
        }
        
        //        if !motionManager.isGyroAvailable {
        //            print("gyro unavailable")
        //        }
        
        if !motionManager.isAccelerometerAvailable && !motionManager.isGyroAvailable {
            return
        }
        
        timer = Timer.scheduledTimer(withTimeInterval: 1 / INFERENCERATE, repeats: true) { timer in
            // initial data gathering for readiness
            if !self.readyForInferencing {
                return
            }
            
            // look backwards to gather sensor data in the last TIMEWINDOW
            // ISSUE: sometimes sensor rate is low due to energy saving and there aren't enough data points
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
            
            // making inference
            let data = preproc(bufAccel)
            if data.count == NFEATURES {
                
                //
                // code from hongyan
                //
                // data processing and model inference
                // convert data to MulArray dtype
                guard let mlMultiArray = try? MLMultiArray(shape:[30], dataType:MLMultiArrayDataType.double) else {
                    fatalError("Unexpected runtime error. MLMultiArray")
                }
                for (index, element) in data.enumerated() {
                    mlMultiArray[index] = NSNumber(floatLiteral: Double(element))
                }
                // predict the data
                guard let modelPrediction = try? self.nnModel.prediction(acc_data: mlMultiArray) else {
                    fatalError("Unexpected runtime error.")
                }
                // convert to decision
                let classPrediction = modelPrediction.class_
                
                // for debug
                print(classPrediction)
                
                // convert class to array
                let decision_array = classPrediction
                let length = classPrediction.count
                let doublePtr =  decision_array.dataPointer.bindMemory(to: Double.self, capacity: length)
                let doubleBuffer = UnsafeBufferPointer(start: doublePtr, count: length)
                let output = Array(doubleBuffer)
                
                //print(output)
                
                // find which class has the highest prob
                let max_ind = output.firstIndex(of: output.max()!)
                
                // need to verify which index in no touching and which is touching
                
                //
                //
                //
                
                //                if classifyByRule(data) {
                if max_ind == 1 {
                    print("Don't touch your face!")
                    for _ in 1...12 {
                        WKInterfaceDevice.current().play(.notification)
                        self.lbWarning.setAlpha(1.0)
                        self.alphaWarning = 1.0
                    }
                    self.bufAccel = []
                    self.readyForInferencing = false
                } else {
                    self.alphaWarning *= 0.95
                    self.lbWarning.setAlpha(self.alphaWarning)
                    //	                    print(FaceOff.getCurrentMillis()%1000)
                }
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
        
        self.timerStub.start()
    }
    
    override func didDeactivate() {
        super.didDeactivate()
        if !FaceOffConfig.ALWAYSON {
            motionManager.stopAccelerometerUpdates()
            timer?.invalidate()
        }
        print("deactivated")
    }
    
}

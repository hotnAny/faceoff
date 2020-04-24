//
//  ORIGINAL:
//  AccelerometerInterfaceController.swift
//  watchOS2Sampler
//
//  Created by Shuichi Tsutsumi on 2015/06/13.
//  Copyright © 2015 Shuichi Tsutsumi. All rights reserved.
//
//  REPURPOSED
//
//
//
import WatchKit
import Foundation
import CoreMotion

class FaceOffTraining: WKInterfaceController{
    
    // overall
    var readyForInferencing :Bool = false
    
    // sensor data
    let SAMPLINGRATE :Double = FaceOffConfig.SAMPLINGRATE
    let INFERENCERATE :Double = 10
    let motionManager = CMMotionManager()
    var bufAccel :[Float] = []
    var tsAccel :[Int64] = []
    var ptrAccel = 0
    var nexamples = 0
    
    // timing
    let TIMEWINDOW = FaceOffConfig.TIMEWINDOW
    var isStarted :Bool = false
    var timeStarted :Int64 = 0
    var timeLastReading :Int64 = 0
    var nframes :Int = 0
    
    //  UI elements
    @IBOutlet weak var btnStart: WKInterfaceButton!
    @IBOutlet weak var lbFPS: WKInterfaceLabel!
    @IBOutlet weak var swTouching: WKInterfaceSwitch!
    @IBOutlet weak var swWild: WKInterfaceSwitch!
    
    // behavior
    var isTouching = true
    var isWild = false
//    var sides = ["Left", "Right"]
//    var partsTouched = ["Hair", "Nose", "Chin", "Eye", "Ear", "Forehead", "Cheek", "Temple", "Mouth"]
//    var how = ["Transiently", "Lingeringly"]
//    var nearMisses = ["Adjust eyeglasses", "Raise hand(s)", "Eat", "Drink", "Listen to cellphone"]
    
    override func awake(withContext context: Any?) {
        super.awake(withContext: context)
        
        motionManager.accelerometerUpdateInterval = 1 / SAMPLINGRATE //0.01s
        swWild.setHidden(isTouching)
        self.refreshStartBtn(FaceOff.getCurrentMillis())
    }
    
    override func willActivate() {
        super.willActivate()
        
        if !motionManager.isAccelerometerAvailable {
            print("accelerometer unavailable!")
            return
        }
        
        // accelerometer event handler
        let handler:CMAccelerometerHandler = {(data: CMAccelerometerData?, error: Error?) -> Void in
            
//             print(data!.acceleration.x, data!.acceleration.y, data!.acceleration.x)
            print(data!.acceleration.z)
            
            // update fps
            let timeThisReading = FaceOff.getCurrentMillis()
            let timeGap = timeThisReading - self.timeLastReading
            if timeGap >= 1000 {
                //                self.lbFPS.setText("FPS: " + (String)(self.nframes))
                //                print("FPS: " + (String)(self.nframes))
                self.nframes = 0
                self.timeLastReading = timeThisReading
            }
            self.nframes += 1
            
            if self.isStarted {
                let timeElapsed = FaceOff.getCurrentMillis() - self.timeStarted
                
                if timeElapsed > self.TIMEWINDOW {
                    self.refreshStartBtn(FaceOff.getCurrentMillis())
                    print(FaceOff.stringize(self.bufAccel) + (self.isTouching ? "Touching" : "NoTouching"))
                    self.bufAccel = []
                    self.nexamples += 1
                    print("# of examples: " + (String)(self.nexamples))
                    self.isStarted = false
                    return
                }
                
                self.bufAccel.append((Float)(data!.acceleration.x))
                self.bufAccel.append((Float)(data!.acceleration.y))
                self.bufAccel.append((Float)(data!.acceleration.z))
            } else if !self.isTouching {
                if self.isWild && timeGap >= 1000 && FaceOff.getCurrentMillis()%3 == 0 {
                    if self.nexamples == FaceOffConfig.NWILDEXAMPLESPER {
//                        self.isWild = false
//                        self.swWild.setOn(false)
                    } else {
                        self.startCollecting()
                    }
                }
            }
        }
        
        // start accelerometer
        motionManager.startAccelerometerUpdates(to: OperationQueue.current!, withHandler: handler)
    }
    
    override func didDeactivate() {
        super.didDeactivate()
        motionManager.stopAccelerometerUpdates()
    }
    
    // start button tap handler
    @IBAction func tapRecognized(_ sender: AnyObject) {
        if(!isTouching && isWild) {
            nexamples = 0
            btnStart.setTitle("Collecting ...")
            return
        }
        
        if !isStarted {
            startCollecting()
        }
    }
    
    // toggle between different class values
    @IBAction func touchSwitchToggled(_ value: Bool) {
        self.isTouching = value
        swWild.setHidden(value)
        self.refreshStartBtn(FaceOff.getCurrentMillis())
        self.nexamples = 0
    }
    
    // toggle between different class values
    @IBAction func wildSwitchToggled(_ value: Bool) {
        self.isWild = value
        self.swTouching.setOn(false)
        self.nexamples = 0
    }
    
    // routine to start data collection
    func startCollecting()->Void{
        btnStart.setTitle("Collecting ...")
        print("collecting ...")
        timeStarted = FaceOff.getCurrentMillis()
        isStarted = true
    }
    
    // update the start button to provide instructions
    func refreshStartBtn(_ n: Int64)->Void{
        if self.isTouching {
            let idx = (Int)(n % (Int64)(FaceOffConfig.PARTSTOUCHED.count))
            let how = FaceOffConfig.HOW[(Int)(FaceOff.getCurrentMillis()%97%2)]
            let side = FaceOffConfig.SIDES[(Int)(FaceOff.getCurrentMillis()%79%2)]
            let info = how + " " + side + " " + FaceOffConfig.PARTSTOUCHED[idx]
            self.btnStart.setTitle(info)
            print(info)
        } else{
            if !self.isWild {
                let idx = (Int)(n % (Int64)(FaceOffConfig.NEARMISSES.count))
                self.btnStart.setTitle(FaceOffConfig.NEARMISSES[idx])
            } else {
                self.btnStart.setTitle("Reset count")
            }
        }
    }
}

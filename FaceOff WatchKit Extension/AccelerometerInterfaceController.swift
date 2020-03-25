//
//  AccelerometerInterfaceController.swift
//  watchOS2Sampler
//
//  Created by Shuichi Tsutsumi on 2015/06/13.
//  Copyright © 2015 Shuichi Tsutsumi. All rights reserved.
//
import WatchKit
import Foundation
import CoreMotion

class AccelerometerInterfaceController: WKInterfaceController{
    
    
    @IBOutlet weak var labelX: WKInterfaceLabel!
    @IBOutlet weak var labelY: WKInterfaceLabel!
    @IBOutlet weak var labelZ: WKInterfaceLabel!
    
    var isTraining :Bool = false;
    var readyForInferencing :Bool = false;
    
    // sensor data
    let SAMPLINGRATE :Double = 100
    let motionManager = CMMotionManager()
    var bufAccel :[Float] = []
    var tsAccel :[Int64] = []
    var ptrAccel = 0
    var nexamples = 0
    
    // timing
    let TIMEWINDOW = 1500
    var isStarted :Bool = false
    var timeStarted :Int64 = 0
    var timeLastReading :Int64 = 0
    var nframes :Int = 0
    
    //  UI elements
    @IBOutlet weak var btnStart: WKInterfaceButton!
    @IBOutlet weak var lbFPS: WKInterfaceLabel!
    @IBOutlet weak var swTouching: WKInterfaceSwitch!
    
    // behavior
    var isTouching = true
    var partsTouched = ["Nose", "Chin", "Left eye", "Right eye", "Ear", "Forehead", "Cheek"]
    
    override func awake(withContext context: Any?) {
        super.awake(withContext: context)
        
        motionManager.accelerometerUpdateInterval = 1 / SAMPLINGRATE //0.01
    }
    
    override func willActivate() {
        super.willActivate()
        
        if motionManager.isAccelerometerAvailable {
            Timer.scheduledTimer(withTimeInterval: 0.1, repeats: true) { timer in
                if(!self.readyForInferencing) {
                    return;
                }
                
                var bufAccel :[Float] = []
                var idx = self.ptrAccel
                let tsCurrent = self.tsAccel[idx/3]
                while(bufAccel.count < self.bufAccel.count) {
                    bufAccel.append(self.bufAccel[idx])
                    bufAccel.append(self.bufAccel[idx+1])
                    bufAccel.append(self.bufAccel[idx+2])
                    
                    idx = (idx + self.bufAccel.count - 3) % self.bufAccel.count
                    let ts = self.tsAccel[idx/3]
                    if(tsCurrent - ts > self.TIMEWINDOW) {
                        print(bufAccel.count)
                        break
                    }
                }
            }
            
            let handler:CMAccelerometerHandler = {(data: CMAccelerometerData?, error: Error?) -> Void in
                
                // update fps
                let timeThisReading = self.getCurrentMillis()
                let timeGap = timeThisReading - self.timeLastReading
                if(timeGap >= 1000) {
                    self.lbFPS.setText("FPS: " + (String)(self.nframes))
                    print("FPS: " + (String)(self.nframes))
                    self.nframes = 0
                    self.timeLastReading = timeThisReading
                }
                self.nframes += 1
                
                if(self.isTraining) {
                    if(self.isStarted) {
                        let timeElapsed = self.getCurrentMillis() - self.timeStarted
                        
                        if(timeElapsed > self.TIMEWINDOW) {
                            self.refreshStartBtn(timeGap)
                            // print(self.stringize(self.bufAccel)+(self.isTouching ? "Touching" : "NoTouching"))
                            print(self.stringize(preproc(self.bufAccel)) + (self.isTouching ? "Touching" : "NoTouching"))
                            self.bufAccel = []
                            self.nexamples += 1
                            print("# of examples: " + (String)(self.nexamples))
                            self.isStarted = false
                            return
                        }
                        
                        self.bufAccel.append((Float)(data!.acceleration.x))
                        self.bufAccel.append((Float)(data!.acceleration.y))
                        self.bufAccel.append((Float)(data!.acceleration.z))
                    } else if(!self.isTouching) {
                        if(timeGap % 197 == 0) {
                            self.startCollecting()
                        }
                    }
                } else{
                    let scaledup = 1.25
                    let interval = 1000 / self.SAMPLINGRATE
                    if(self.bufAccel.count < (Int)((Double)(3 * self.TIMEWINDOW) * scaledup / interval)) {
                        self.bufAccel.append((Float)(data!.acceleration.x))
                        self.bufAccel.append((Float)(data!.acceleration.y))
                        self.bufAccel.append((Float)(data!.acceleration.z))
                        self.tsAccel.append(self.getCurrentMillis())
                        self.ptrAccel = self.bufAccel.count
                        //                        print(self.bufAccel.count)
                    } else {
                        self.readyForInferencing = true;
                        let idx = (self.ptrAccel + 3) % self.bufAccel.count
                        self.bufAccel[idx] = (Float)(data!.acceleration.x)
                        self.bufAccel[idx + 1] = (Float)(data!.acceleration.y)
                        self.bufAccel[idx + 2] = (Float)(data!.acceleration.z)
                        self.tsAccel[idx / 3] = self.getCurrentMillis()
                        self.ptrAccel = idx
                        //                        print(self.bufAccel.count)
                        
                    }
                    //                    print(self.ptrAccel)
                }
            }
            motionManager.startAccelerometerUpdates(to: OperationQueue.current!, withHandler: handler)
        }
        else {
            print("acclerometer not available")
        }
    }
    
    override func didDeactivate() {
        super.didDeactivate()
        
        motionManager.stopAccelerometerUpdates()
    }
    
    @IBAction func tapRecognized(_ sender: AnyObject) {
        if(!isStarted) {
            startCollecting()
        }
    }
    
    @IBAction func switchToggled(_ value: Bool) {
        self.isTouching = value
    }
    
    func getCurrentMillis()->Int64{
        return Int64(NSDate().timeIntervalSince1970 * 1000)
    }
    
    func startCollecting()->Void{
        btnStart.setTitle("Collecting")
        print("collecting ...")
        timeStarted = getCurrentMillis()
        isStarted = true
    }
    
    func stringize(_ nums: [Float])->String{
        var str = ""
        for x in nums {
            str += String(format: "%.3f", x) + ","
        }
        return str
    }
    
    func refreshStartBtn(_ n: Int64)->Void{
        if(self.isTouching) {
            let idx = (Int)(n % (Int64)(self.partsTouched.count))
            self.btnStart.setTitle(self.partsTouched[idx])
        } else{
            self.btnStart.setTitle("No touch")
        }
    }
    
}

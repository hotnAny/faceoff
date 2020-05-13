//
//  FaceOffRecycled.swift
//  FaceOff WatchKit Extension
//
//  Created by Xiang 'Anthony' Chen on 4/15/20.
//  Copyright © 2020 Xiang 'Anthony' Chen. All rights reserved.
//

import Foundation


     
     //                else {
     //                    if FaceOff.getCurrentMillis() - self.timeLastNonActionMark >= 1000 {
     //                        // print(FaceOff.stringize(bufAccel) + "No Touching")
     //                        print(String(Int(timeSinceLastAction/1000)) + ": No Touching")
     //                        self.timeLastNonActionMark = FaceOff.getCurrentMillis()
     //                    }
     //                }
     
     //                let n = 8
     //                let ratioLowered = 1 - Double(n/2) / self.INFERENCERATE
     //                let m = Double(self.actionInterval) * (1-ratioLowered) / (1000 / self.INFERENCERATE)
     //                if  timeSinceLastAction >= Int64(Double(self.actionInterval) * ratioLowered) && Int.random(in: 0..<Int(m)) == 0 {
     
     
     
     // making inference
     
//func makeInference(data: [Float]) {
//    let data = preproc(bufAccel)
//    if data.count == NFEATURES {
//        
//        //
//        // code from hongyan
//        //
//        // data processing and model inference
//        // convert data to MulArray dtype
//        guard let mlMultiArray = try? MLMultiArray(shape:[30], dataType:MLMultiArrayDataType.double) else {
//            fatalError("Unexpected runtime error. MLMultiArray")
//        }
//        for (index, element) in data.enumerated() {
//            mlMultiArray[index] = NSNumber(floatLiteral: Double(element))
//        }
//        // predict the data
//        guard let modelPrediction = try? self.nnModel.prediction(acc_data: mlMultiArray) else {
//            fatalError("Unexpected runtime error.")
//        }
//        // convert to decision
//        let classPrediction = modelPrediction.class_
//        
//        // for debug
//        //                print(classPrediction)
//        
//        // convert class to array
//        let decision_array = classPrediction
//        let length = classPrediction.count
//        let doublePtr =  decision_array.dataPointer.bindMemory(to: Double.self, capacity: length)
//        let doubleBuffer = UnsafeBufferPointer(start: doublePtr, count: length)
//        let output = Array(doubleBuffer)
//        
//        //print(output)
//        
//        // need to verify which index in no touching and which is touching
//        
//        if (Double)(output.max() ?? 0) > 0.9 {
//            // find which class has the highest prob
//            let max_ind = output.firstIndex(of: output.max()!)
//            
//            if max_ind == 1 {
//                print("Don't touch your face!")
//                print(classPrediction)
//                for _ in 1...12 {
//                    WKInterfaceDevice.current().play(.notification)
//                }
//                self.lbWarning.setAlpha(1.0)
//                self.alphaWarning = 1.0
//                self.bufAccel = []
//                self.readyForInferencing = false
//            } else {
//                self.alphaWarning *= 0.95
//                self.lbWarning.setAlpha(self.alphaWarning)
//            }
//            
//        }
//        
//    }
//}

//                if self.countActions == self.NACTIONSPERTASK {
               //                    self.countActions = 0
               //                    self.swTesting.setOn(false)
               //                    self.testingToggled(false)
               //                    // print(Int64(FaceOff.getCurrentMillis() - self.timeTestingStarted) / 1000)
               //                }


//
              // code from hongyan
              //
              // data processing and model inference
              // convert data to MulArray dtype
              //            guard let mlMultiArray = try? MLMultiArray(shape:[30], dataType:MLMultiArrayDataType.double) else {
              //                fatalError("Unexpected runtime error. MLMultiArray")
              //            }
              //            for (index, element) in data.enumerated() {
              //                mlMultiArray[index] = NSNumber(floatLiteral: Double(element))
              //            }
              //            // predict the data
              //            guard let modelPrediction = try? self.nnModel.prediction(acc_data: mlMultiArray) else {
              //                fatalError("Unexpected runtime error.")
              //            }
              //            // convert to decision
              //            let classPrediction = modelPrediction.class_
              //
              //            // for debug
              //            //                print(classPrediction)
              //
              //            // convert class to array
              //            let decision_array = classPrediction
              //            let length = classPrediction.count
              //            let doublePtr =  decision_array.dataPointer.bindMemory(to: Double.self, capacity: length)
              //            let doubleBuffer = UnsafeBufferPointer(start: doublePtr, count: length)
              //            let output = Array(doubleBuffer)
              //
              //            //print(output)
              //
              //            // need to verify which index in no touching and which is touching
              //
              //            if (Double)(output.max() ?? 0) > 0.9 {
              
              // find which class has the highest prob
              //                let max_ind = output.firstIndex(of: output.max()!)

//
//  FaceOffConfig.swift
//  FaceOff WatchKit Extension
//
//  Created by Xiang 'Anthony' Chen on 3/25/20.
//  Copyright © 2020 Xiang 'Anthony' Chen. All rights reserved.
//

import Foundation

final class FaceOffConfig {
    static let SAMPLINGRATE :Double = 100
    static let INFERENCERATE :Double = 10
    static let TIMEWINDOW = 1500
    static let ALWAYSON = false
    static let NWILDEXAMPLESPER = 10
    
    static let SIDES = ["Left", "Right"]
    static let PARTSTOUCHED = ["Hair", "Nose", "Chin", "Eye", "Ear", "Forehead", "Cheek", "Temple", "Mouth"]
    static let HOW = ["Transiently", "Lingeringly"]
    static let NEARMISSES = ["Eyeglasses", "Raise hand", "Eat", "Drink", "Pick up phone"]
    
//    static let UPARTSTOUCHED = ["Backhead", "Nose", "Chin", "Eye", "Ear"]
//    static let UPARTSTOUCHED = ["Hair", "Nose", "Chin", "Cheek", "Ear"]
    static let UPARTSTOUCHED = ["Forehead", "Nose", "Cheek", "Eye", "Ear"]
}

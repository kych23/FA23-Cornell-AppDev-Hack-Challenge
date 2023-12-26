//
//  LoginVC.swift
//  LatteLink
//
//  Created by Kyle Chu on 12/25/23.

//  minimize all functions: (Cmd + Shift + Option + <-)

import UIKit
import SnapKit
import Alamofire

class LoginVC: UIViewController {
    
    // MARK: - Properties (Subviews)
    private let emailText = UILabel()
    private let pwdText = UILabel()
    private let emailBox = UITextField()
    private let pwdBox = UITextField()
    private let logo = UIImageView()
    private let centerText = UILabel()
    private let enterButton = UIButton()
    private let newAccButton = UIButton()
    
    // MARK: - Properties (Data)
    
    
    
    // MARK: - viewDidLoad
    override func viewDidLoad() {
        super.viewDidLoad()
        view.layer.backgroundColor = UIColor(red: 1, green: 1, blue: 1, alpha: 1).cgColor
        
        setupCenterText()
        setupLogo()
        setupEmailSection()
        setupPwdSection()
        setupButtons()
    }
    
    // MARK: - Setup the views
    private func setupEmailSection(){
        // Text Field's properties
        emailBox.font = UIFont(name: "Roboto-Light", size: 20)
        emailBox.frame = CGRect(x: 0, y: 0, width: 300, height: 45)
        emailBox.textColor = UIColor(red: 0.35, green: 0.18, blue: 0.05, alpha: 1)
        emailBox.borderStyle = .roundedRect
        emailBox.keyboardType = .default
        emailBox.backgroundColor = UIColor(red: 0.973, green: 0.953, blue: 0.937, alpha: 0.7)
        
        // creates the gradient color and border using the static function
        let gradientColor = UIColor(patternImage: LoginVC.gradientImage(bounds: emailBox.bounds, colors: [UIColor(red: 0.87, green: 0.72, blue: 0.65, alpha: 1), UIColor(red: 0.6, green: 0.62, blue: 0.55, alpha: 0.53)]))
        emailBox.layer.borderColor = gradientColor.cgColor
        emailBox.layer.borderWidth = 3
        emailBox.layer.cornerRadius = 4.22
        
        view.addSubview(emailBox)
        emailBox.snp.makeConstraints { make in
            make.centerX.equalToSuperview()
            make.centerY.equalTo(centerText.snp.centerY).offset(100)
            make.width.equalTo(300)
        }
        
        // Text Box's properties
        emailText.text = "Your Email"
        emailText.textColor = UIColor(red: 0.35, green: 0.18, blue: 0.05, alpha: 1)
        emailText.font = UIFont(name: "Roboto-Medium", size: 14)
        emailText.frame = CGRect(x: 0, y: 0, width: 50, height: 10)
        emailText.textAlignment = .left

        view.addSubview(emailText)
        emailText.snp.makeConstraints { make in
            make.bottom.equalTo(emailBox.snp.top).offset(-10)
            make.leading.equalTo(emailBox.snp.leading)
            make.height.equalTo(16)
            make.width.equalTo(68)
        }
    }
    
    private func setupPwdSection() {
        
    }
    
    private func setupLogo() {
        logo.image = UIImage(named: "Logo")
        //logo.contentMode = .scaleAspectFit
        logo.frame = CGRect(x: 0, y: 0, width: 10, height: 10)
        logo.layer.cornerRadius = 10
        
        view.addSubview(logo)
        
        logo.snp.makeConstraints { make in
            make.centerX.equalToSuperview()
            make.bottom.equalTo(centerText.snp.top).offset(-40)
        }
    }
    
    private func setupCenterText() {
        centerText.frame = CGRect(x: 0, y: 0, width: 50, height: 50)
        centerText.font = UIFont(name: "Roboto-Bold", size: 30)
        centerText.numberOfLines = 0
        centerText.lineBreakMode = .byWordWrapping
        centerText.textColor = UIColor(red: 0.35, green: 0.18, blue: 0.05, alpha: 1)
        centerText.textAlignment = .center
        centerText.text = "Welcome to\nLatte Link!"

        view.addSubview(centerText)
        
        centerText.snp.makeConstraints { make in
            make.centerX.equalToSuperview()
            make.centerY.equalToSuperview().offset(-70)
        }

    }
    
    private func setupButtons() {
        
    }
    
}

// Function that creates a gradient border
extension LoginVC {
    static func gradientImage(bounds: CGRect, colors: [UIColor]) -> UIImage {
        let gradientLayer = CAGradientLayer()
        gradientLayer.frame = bounds
        gradientLayer.colors = colors.map(\.cgColor)
        
        // This makes it left to right, default is top to bottom
        gradientLayer.startPoint = CGPoint(x: 0.0, y: 0.5)
        gradientLayer.endPoint = CGPoint(x: 1.0, y: 0.5)
        
        let renderer = UIGraphicsImageRenderer(bounds: bounds)
        
        return renderer.image { ctx in gradientLayer.render(in: ctx.cgContext)
        }
    }
}

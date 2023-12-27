//
//  LoginVC.swift
//  LatteLink
//
//  Created by Kyle Chu on 12/25/23.

//  iOS 15 simulator ->        W: 393.0       H: 852.0
//  minimize all functions: (Cmd + Shift + Option + <-)

import UIKit
import SnapKit
import Alamofire

func gradientImage(bounds: CGRect, colors: [UIColor]) -> UIImage {
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
class LoginVC: UIViewController {
    // MARK: - Properties (Subviews)
    private let emailText = UILabel()
    private let pwdText = UILabel()
    private let emailBox = UITextField()
    private let pwdBox = UITextField()
    private let topAccent = UIImageView()
    private let logo = UIImageView()
    private let centerText = UILabel()
    private let loginButton = UIButton()
    private let newAccButton = UIButton()
    
    // MARK: - Properties (Data)
    private var loginButtonText = "Create Account"
    
    // MARK: - viewDidLoad
    override func viewDidLoad() {
        super.viewDidLoad()
        view.layer.backgroundColor = UIColor(red: 1, green: 1, blue: 1, alpha: 1).cgColor
        
        setupTopAccent()
        setupCenterText()
        setupLogo()
        setupEmailSection()
        setupPwdSection()
        setupButtons()
    }
    
    // MARK: - Setup the views
    private func setupTopAccent(){
        topAccent.image = UIImage(named: "Accent")
        topAccent.contentMode = .scaleAspectFit
        topAccent.layer.cornerRadius = 10
        
        view.addSubview(topAccent)
        
        topAccent.snp.makeConstraints { make in
            make.top.equalTo(view.snp.top).offset(10)
            make.trailing.equalTo(view.snp.trailing)
            make.height.equalTo(230)
            make.width.equalTo(237)
        }
    }
    
    private func setupEmailSection(){
        // Text Field's properties
        emailBox.font = UIFont(name: "Roboto-Light", size: 15)
        emailBox.frame = CGRect(x: 0, y: 0, width: 280, height: 45)
        emailBox.textColor = UIColor(red: 0.35, green: 0.18, blue: 0.05, alpha: 1)
        emailBox.borderStyle = .roundedRect
        emailBox.keyboardType = .default
        emailBox.backgroundColor = UIColor(red: 0.973, green: 0.953, blue: 0.937, alpha: 0.7)
        
        // creates the gradient color and border using the static function
        let gradientColor = UIColor(patternImage: gradientImage(bounds: emailBox.bounds, colors: [UIColor(red: 0.6, green: 0.62, blue: 0.55, alpha: 0.8), UIColor(red: 0.84, green: 0.74, blue: 0.65, alpha: 1)]))
        emailBox.layer.borderColor = gradientColor.cgColor
        emailBox.layer.borderWidth = 2
        emailBox.layer.cornerRadius = 4.22
        
        view.addSubview(emailBox)
        emailBox.snp.makeConstraints { make in
            make.centerX.equalToSuperview()
            make.centerY.equalTo(centerText.snp.centerY).offset(100)
            make.width.equalTo(280)
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
            make.width.equalTo(100)
        }
    }
    
    private func setupPwdSection() {
        // Text Field's properties
        pwdBox.font = UIFont(name: "Roboto-Light", size: 15)
        pwdBox.frame = CGRect(x: 0, y: 0, width: 280, height: 45)
        pwdBox.textColor = UIColor(red: 0.35, green: 0.18, blue: 0.05, alpha: 1)
        pwdBox.borderStyle = .roundedRect
        pwdBox.keyboardType = .default
        pwdBox.backgroundColor = UIColor(red: 0.973, green: 0.953, blue: 0.937, alpha: 0.7)
        
        // creates the gradient color and border using the static function
        let gradientColor = UIColor(patternImage: gradientImage(bounds: pwdBox.bounds, colors: [UIColor(red: 0.84, green: 0.74, blue: 0.65, alpha: 1), UIColor(red: 0.6, green: 0.62, blue: 0.55, alpha: 0.8)]))
        pwdBox.layer.borderColor = gradientColor.cgColor
        pwdBox.layer.borderWidth = 2
        pwdBox.layer.cornerRadius = 4.22
        
        view.addSubview(pwdBox)
        pwdBox.snp.makeConstraints { make in
            make.centerX.equalToSuperview()
            make.centerY.equalTo(emailBox.snp.centerY).offset(80)
            make.width.equalTo(280)
        }
        
        // Text Box's properties
        pwdText.text = "Your Password"
        pwdText.textColor = UIColor(red: 0.35, green: 0.18, blue: 0.05, alpha: 1)
        pwdText.font = UIFont(name: "Roboto-Medium", size: 14)
        pwdText.frame = CGRect(x: 0, y: 0, width: 50, height: 10)
        pwdText.textAlignment = .left
        
        view.addSubview(pwdText)
        pwdText.snp.makeConstraints { make in
            make.bottom.equalTo(pwdBox.snp.top).offset(-10)
            make.leading.equalTo(pwdBox.snp.leading)
            make.height.equalTo(16)
            make.width.equalTo(100)
        }
    }
    
    private func setupLogo() {
        logo.image = UIImage(named: "Logo")
        logo.contentMode = .scaleAspectFit
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
            make.centerY.equalToSuperview().offset(-59)
        }
        
    }
    
    private func setupButtons() {
        // Create Account Button
        loginButton.setTitle("Create Account", for: .normal)
        loginButton.titleLabel?.font = UIFont(name: "Roboto-Medium", size: 16)
        loginButton.setTitleColor(UIColor(red: 0.35, green: 0.38, blue: 0.31, alpha: 1), for: .normal)
        loginButton.backgroundColor = UIColor(red: 0.89, green: 0.89, blue: 0.79, alpha: 0.8)
        loginButton.layer.cornerRadius = 10
        loginButton.layer.borderWidth = 1
        loginButton.layer.borderColor = UIColor(red: 0.482, green: 0.529, blue: 0.427, alpha: 0.5).cgColor
        
        loginButton.addTarget(self, action:#selector(pushVC), for: .touchUpInside)
        
        view.addSubview(loginButton)
        loginButton.snp.makeConstraints { make in
            make.centerX.equalToSuperview()
            make.centerY.equalTo(pwdBox.snp.centerY).offset(80)
            make.width.equalTo(160)
            make.height.equalTo(34)
        }
        
        // New Account Button
        let yourAttributes: [NSAttributedString.Key: Any] = [
             .font: UIFont(name: "Roboto-Light", size: 12)!,
             .foregroundColor: UIColor(red: 0.345, green: 0.184, blue: 0.055, alpha: 1),
             .underlineStyle: NSUnderlineStyle.single.rawValue
         ]
        let attributedTitle = NSAttributedString(string: "I already have an account...", attributes: yourAttributes)
        newAccButton.setAttributedTitle(attributedTitle, for: .normal)
        
        newAccButton.addTarget(self, action: #selector(pushVC), for: .touchUpInside)
        
        view.addSubview(newAccButton)
        newAccButton.snp.makeConstraints { make in
            make.centerX.equalToSuperview()
            make.centerY.equalTo(pwdBox.snp.centerY).offset(240)
            make.width.equalTo(143)
            make.height.equalTo(14)
        }
    }
    
    // MARK: - button helper methods
    @objc private func pushVC(_ VC: UIViewController){
        //let VCtoBePushed = NewAccVC(text: text, delegate: self)
        //navigationController?.pushViewController(VCtoBePushed, animated: true)
    }
}


    

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

extension UIViewController {
    // contains a dictionary of the UIButton instance to its UIViewController that it pushes
    static var buttonVCMap: [UIButton: UIViewController.Type] = [:]
    
    @objc func pushVC(_ sender: UIButton) {
        if let vcType = UIViewController.buttonVCMap[sender] {
            let vc = vcType.init()
            navigationController?.pushViewController(vc, animated: true)
        }
    }
    
    @objc func popVC() {
        navigationController?.popViewController(animated: true)
    }
}

class LoginVC: UIViewController {
    // MARK: - Properties (Subviews)
    private let topAccent = UIImageView()
    private let logo = UIImageView()
    private let centerText = UILabel()
    private let emailText = UILabel()
    private let pwdText = UILabel()
    private var emailBox = UITextField()
    private var pwdBox = UITextField()
    private var underlinedButton = UIButton()
    private var greenButton = UIButton()
    
    // MARK: - Properties (Data)
    private var loginButtonText = "Create Account"
    // true for if the current page is login, false if the current page is create
    public var login: Bool = true
    
    
    // MARK: - viewDidLoad
    override func viewDidLoad() {
        super.viewDidLoad()
        view.layer.backgroundColor = UIColor(red: 1, green: 1, blue: 1, alpha: 1).cgColor
        self.navigationItem.hidesBackButton = true
        setupTopAccent()
        setupCenterText()
        setupLogo()
        setupEmailSection()
        setupPwdSection()
        setupCustomButton()
        setupUnderlinedButton()
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

    private func setupEmailSection(){
        emailBox = CustomTextField(font: UIFont(name: "Roboto-Light", size: 15)!, width: 299, height: 37)
        view.addSubview(emailBox)
        emailBox.snp.makeConstraints { make in
            make.centerX.equalToSuperview()
            make.centerY.equalTo(centerText.snp.centerY).offset(100)
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
        pwdBox = CustomTextField(font: UIFont(name: "Roboto-Light", size: 15)!, width: 299, height: 37)
        view.addSubview(pwdBox)
        pwdBox.snp.makeConstraints { make in
            make.centerX.equalToSuperview()
            make.centerY.equalTo(emailBox.snp.centerY).offset(80)
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
    
    private func setupCustomButton() {
        // Green Button
        greenButton = CustomButton(title: "Create Account", width: 160, height: 34)
        greenButton.addTarget(self, action: #selector(pushVC(_:)), for: .touchUpInside)
        UIViewController.buttonVCMap[greenButton] = NewAccVC.self
        
        view.addSubview(greenButton)
        greenButton.snp.makeConstraints { make in
            make.centerX.equalToSuperview()
            make.centerY.equalTo(pwdBox.snp.centerY).offset(80)
        }
    }
    private func setupUnderlinedButton() {
        // Underlined Button
        let yourAttributes: [NSAttributedString.Key: Any] = [
             .font: UIFont(name: "Roboto-Light", size: 12)!,
             .foregroundColor: UIColor(red: 0.345, green: 0.184, blue: 0.055, alpha: 1),
             .underlineStyle: NSUnderlineStyle.single.rawValue
         ]
        let attributedTitle = NSAttributedString(string: "I already have an account...", attributes: yourAttributes)
        underlinedButton.setAttributedTitle(attributedTitle, for: .normal)
        underlinedButton.addTarget(self, action: #selector(swapUI), for: .touchUpInside)
        
        view.addSubview(underlinedButton)
        underlinedButton.snp.makeConstraints { make in
            make.centerX.equalToSuperview()
            make.centerY.equalTo(pwdBox.snp.centerY).offset(240)
            make.width.equalTo(143)
            make.height.equalTo(14)
        }
    }
    
    // MARK: - changes the subviews from login account to create account or vice versa
    @objc internal func swapUI() {
        if login {
            // changes text
            centerText.text = "Welcome Back to\nLatte Link!"
            // swaps the bottom, underlined buttom
            let yourAttributes: [NSAttributedString.Key: Any] = [
                 .font: UIFont(name: "Roboto-Light", size: 12)!,
                 .foregroundColor: UIColor(red: 0.345, green: 0.184, blue: 0.055, alpha: 1),
                 .underlineStyle: NSUnderlineStyle.single.rawValue
            ]
            let attributedTitle = NSAttributedString(string: "I don't have an account...", attributes: yourAttributes)
            underlinedButton.setAttributedTitle(attributedTitle, for: .normal)
            // swaps the login button to create
            greenButton.setTitle("Sign In", for: .normal)
            greenButton.addTarget(self, action: #selector(pushVC(_:)), for: .touchUpInside)
            UIViewController.buttonVCMap[greenButton] = HomeVC.self
            login = false
        } else {
            setupCenterText()
            setupUnderlinedButton()
            greenButton.setTitle("Create Account", for: .normal)
            UIViewController.buttonVCMap[greenButton] = NewAccVC.self
            login = true
        }
    }
    
}

class CustomTextField: UITextField {
    init(font: UIFont, width: Int, height: Int) {
        super.init(frame: .zero)
        self.font = font
        self.textColor = UIColor(red: 0.35, green: 0.18, blue: 0.05, alpha: 1)
        self.borderStyle = .roundedRect
        self.keyboardType = .default
        self.autocapitalizationType = .none
        self.backgroundColor = UIColor(red: 0.973, green: 0.953, blue: 0.937, alpha: 0.7)
        self.layer.cornerRadius = 4.22
        let gradientColor = UIColor(patternImage: gradientImage(bounds: self.bounds, colors: [UIColor(red: 0.6, green: 0.62, blue: 0.55, alpha: 0.8), UIColor(red: 0.84, green: 0.74, blue: 0.65, alpha: 1)]))
        self.layer.borderColor = gradientColor.cgColor
        self.layer.borderWidth = 2

        self.snp.makeConstraints { make in
            make.width.equalTo(width)
            make.height.equalTo(height)
        }
    }
    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
    private func gradientImage(bounds: CGRect, colors: [UIColor]) -> UIImage {
        let gradientLayer = CAGradientLayer()
        gradientLayer.frame = bounds
        gradientLayer.colors = colors.map(\.cgColor)

        // This makes it left to right, default is top to bottom
        gradientLayer.startPoint = CGPoint(x: Double.random(in:0.0...1.0), y: Double.random(in:0.0...1.0))
        gradientLayer.endPoint = CGPoint(x: Double.random(in:0.0...1.0), y: Double.random(in:0.0...1.0))

        let renderer = UIGraphicsImageRenderer(bounds: bounds)
        return renderer.image { ctx in gradientLayer.render(in: ctx.cgContext)
        }
    }
}

class CustomButton: UIButton {
    init(title: String, width: Int, height: Int) {
        super.init(frame: .zero)
        self.setTitle(title, for: .normal)
        self.titleLabel?.font = UIFont(name: "Roboto-Medium", size: 16)
        self.setTitleColor(UIColor(red: 0.345, green: 0.192, blue: 0.004, alpha: 1), for: .normal)
        self.backgroundColor = UIColor(red: 0.89, green: 0.89, blue: 0.79, alpha: 0.8)
        self.layer.cornerRadius = 10
        self.layer.borderWidth = 1
        self.layer.borderColor = UIColor(red: 0.482, green: 0.529, blue: 0.427, alpha: 0.5).cgColor
        self.snp.makeConstraints { make in
            make.width.equalTo(width)
            make.height.equalTo(height)
        }
    }
    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
}

class CustomTextView: UITextView {
    init(font: UIFont, width: Int, height: Int) {
        super.init(frame: .zero, textContainer: nil)
        self.font = font
        self.textColor = UIColor(red: 0.35, green: 0.18, blue: 0.05, alpha: 1)
        self.keyboardType = .default
        self.autocapitalizationType = .none
        self.backgroundColor = UIColor(red: 0.973, green: 0.953, blue: 0.937, alpha: 0.7)
//        let gradientColor = UIColor(patternImage: gradientImage(bounds: self.bounds, colors: [UIColor(red: 0.6, green: 0.62, blue: 0.55, alpha: 0.8), UIColor(red: 0.84, green: 0.74, blue: 0.65, alpha: 1)]))
        //self.layer.borderColor = gradientColor.cgColor
       // self.layer.borderWidth = 2
        self.layer.cornerRadius = 8
        self.layer.masksToBounds = true
        self.isScrollEnabled = true

        self.snp.makeConstraints { make in
            make.width.equalTo(width)
            make.height.equalTo(height)
        }
        
        addGradientBorder(width: CGFloat(width), height: CGFloat(height), colors: [
        UIColor(red: 0.6, green: 0.62, blue: 0.55, alpha: 0.8),
        UIColor(red: 0.84, green: 0.74, blue: 0.65, alpha: 1)
        ])
    }
    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
//   private func gradientImage(bounds: CGRect, colors: [UIColor]) -> UIImage {
//        let gradientLayer = CAGradientLayer()
//        gradientLayer.frame = bounds
//        gradientLayer.colors = colors.map(\.cgColor)
//
//        // This makes it left to right, default is top to bottom
//        gradientLayer.startPoint = CGPoint(x: Double.random(in:0.0...1.0), y: Double.random(in:0.0...1.0))
//        gradientLayer.endPoint = CGPoint(x: Double.random(in:0.0...1.0), y: Double.random(in:0.0...1.0))
//
//        let renderer = UIGraphicsImageRenderer(bounds: bounds)
//        return renderer.image { ctx in gradientLayer.render(in: ctx.cgContext)
//        }
//    }
    private func addGradientBorder(width: CGFloat, height: CGFloat, colors: [UIColor]) {
    let gradientLayer = CAGradientLayer()
    gradientLayer.frame = CGRect(x: 0, y: 0, width: width, height: height)
    gradientLayer.colors = colors.map(\.cgColor)
    gradientLayer.startPoint = CGPoint(x: 0, y: 0.5)
    gradientLayer.endPoint = CGPoint(x: 1, y: 0.5)
    gradientLayer.cornerRadius = layer.cornerRadius

    let shape = CAShapeLayer()
    shape.lineWidth = 1
    shape.path = UIBezierPath(roundedRect: bounds, cornerRadius: layer.cornerRadius).cgPath
    shape.strokeColor = UIColor.black.cgColor
    shape.fillColor = UIColor.clear.cgColor
    gradientLayer.mask = shape

    layer.addSublayer(gradientLayer)
    }
}

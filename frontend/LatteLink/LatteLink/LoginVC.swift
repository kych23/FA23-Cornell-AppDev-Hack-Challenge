//
//  LoginVC.swift
//  LatteLink
//
//  Created by Kyle Chu on 12/25/23.

//  minimize all functions: (Cmd + Shift + Option + <-)

import UIKit

class LoginVC: UIViewController {
    
    // MARK: - Properties (Subviews)
    private let emailText = UILabel()
    private let pwdText = UILabel()
    private let emailBox = UITextField()
    private let pwdBox = UITextField()
    private let logo = UIImage()
    private let centerText = UILabel()
    private let enterButton = UIButton()
    private let newAccButton = UIButton()
    
    // MARK: - viewDidLoad
    override func viewDidLoad() {
        super.viewDidLoad()
        title = "Login Page"
        view.layer.backgroundColor = UIColor(red: 1, green: 1, blue: 1, alpha: 1).cgColor
        
        setupCenterText()
        setupEmailSection()
    }
    
    // MARK: - Setup the views
    private func setupEmailSection(){
        // Text Box's properties
        emailText.text = "Your Email"
        emailText.textColor = UIColor(red: 0.345, green: 0.184, blue: 0.055, alpha: 1)
        emailText.font = UIFont(name: "Roboto-Medium", size: 14)
        emailText.frame = CGRect(x: 0, y: 0, width: 274, height: 16)
        emailText.textAlignment = .left

        view.addSubview(emailText)
        emailText.translatesAutoresizingMaskIntoConstraints = false

        NSLayoutConstraint.activate([
            emailText.topAnchor.constraint(equalTo: centerText.bottomAnchor, constant: 20),
            emailText.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            emailText.widthAnchor.constraint(equalToConstant: 68),
            emailText.heightAnchor.constraint(equalToConstant: 16)
        ])
        
        // Text Field's properties
        emailBox.font = .systemFont(ofSize: 24)
        emailBox.frame = CGRect(x: 0, y: 0, width: 274, height: 35)
        emailBox.textColor = UIColor.black
        emailBox.layer.borderColor = UIColor(red: 0.85, green: 0.85, blue: 0.85, alpha: 0).cgColor
        
        // creates the inner text field color
        let insideLayer = CALayer()
        insideLayer.backgroundColor = UIColor(red: 0.973, green: 0.953, blue: 0.937, alpha: 0.7).cgColor
        insideLayer.bounds = emailBox.bounds
        insideLayer.position = emailBox.center
        emailBox.layer.cornerRadius = 4.22
        emailBox.layer.addSublayer(insideLayer)

        view.addSubview(emailBox)
        emailBox.translatesAutoresizingMaskIntoConstraints = false

        // Constraints
        NSLayoutConstraint.activate([
            emailBox.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            emailBox.topAnchor.constraint(equalTo: emailText.bottomAnchor),
            emailBox.widthAnchor.constraint(equalToConstant: 274)
        ])
    }
    
    private func setupPwdBox() {
        
    }
    
    private func setupLogo() {
        
    }
    
    private func setupCenterText() {
        centerText.frame = CGRect(x: 0, y: 0, width: 234.46, height: 66)
        centerText.font = UIFont(name: "Roboto-Bold", size: 28) ?? .systemFont(ofSize: 28)
        centerText.numberOfLines = 0
        centerText.lineBreakMode = .byWordWrapping
        centerText.textColor = UIColor(red: 0.35, green: 0.18, blue: 0.05, alpha: 1)
        // Line height: 32.81 pt
        centerText.textAlignment = .center
        centerText.text = "Welcome to\nLatte Link!"

        view.addSubview(centerText)
        centerText.translatesAutoresizingMaskIntoConstraints = false
        
        NSLayoutConstraint.activate([
            centerText.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            centerText.centerYAnchor.constraint(equalTo: view.centerYAnchor),
            centerText.widthAnchor.constraint(equalToConstant: 234.46),
            centerText.heightAnchor.constraint(equalToConstant: 66)
        ])

    }
    
    private func setupEnterButton() {
        
    }
    
    private func setupNewAccButton() {
        
    }
}

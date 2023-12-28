//
//  NewAccVC.swift
//  LatteLink
//
//  Created by Kyle Chu on 12/27/23.
//
import UIKit
import SnapKit
import Alamofire

class NewAccVC: UIViewController {
    // MARK: - Properties (Subviews)
    private let topAccent = UIImageView()
    private let logo = UIImageView()    
    private let centerText = UILabel()
    
    private let loginButton = UIButton()
    private let userButton = UIButton()
    private let orgButton = UIButton()
    private let backButton = UIButton()
    
    // MARK:  Properties (data)
    private var text: String = ""

    // loads the view
    override func viewDidLoad() {
        super.viewDidLoad()
        view.layer.backgroundColor = UIColor(red: 1, green: 1, blue: 1, alpha: 1).cgColor
        
        setupTopAccent()
        setupCenterText()
        setupLogo()
        setupButtons()
    }
    
    // MARK: - Setup views
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
        centerText.text = "Are you creating an\naccount for..."
        
        view.addSubview(centerText)
        
        centerText.snp.makeConstraints { make in
            make.centerX.equalToSuperview()
            make.centerY.equalToSuperview().offset(-59)
        }
        
    }
    
    private func setupButtons() {
        // Login Button
        let yourAttributes: [NSAttributedString.Key: Any] = [
             .font: UIFont(name: "Roboto-Light", size: 12)!,
             .foregroundColor: UIColor(red: 0.345, green: 0.184, blue: 0.055, alpha: 1),
             .underlineStyle: NSUnderlineStyle.single.rawValue
         ]
        let attributedTitle = NSAttributedString(string: "I already have an account...", attributes: yourAttributes)
        loginButton.setAttributedTitle(attributedTitle, for: .normal)
        loginButton.addTarget(self, action: #selector(pushVC), for: .touchUpInside)
        view.addSubview(loginButton)
        loginButton.snp.makeConstraints { make in
            make.centerX.equalToSuperview()
            make.centerY.equalTo(view.snp.bottom).offset(-58)
            make.width.equalTo(143)
            make.height.equalTo(14)
        }
        
        // Back Button
        backButton.setImage(UIImage(named: "LeftArrow"), for: .normal)
        backButton.addTarget(self, action:#selector(pushVC), for: .touchUpInside)
        view.addSubview(backButton)
        backButton.snp.makeConstraints { make in
            make.leading.equalTo(view.snp.leading).offset(35)
            make.top.equalTo(view.snp.top).offset(89)
            make.width.equalTo(26)
            make.height.equalTo(26)
        }
        
        // User Button
        userButton.setTitle("Yourself", for: .normal)
        userButton.titleLabel?.font = UIFont(name: "Roboto-Medium", size: 16)
        userButton.setTitleColor(UIColor(red: 0.345, green: 0.192, blue: 0.004, alpha: 1), for: .normal)
        userButton.backgroundColor = UIColor(red: 0.89, green: 0.89, blue: 0.79, alpha: 0.8)
        userButton.layer.cornerRadius = 10
        userButton.layer.borderWidth = 1
        userButton.layer.borderColor = UIColor(red: 0.482, green: 0.529, blue: 0.427, alpha: 0.5).cgColor
        
        userButton.addTarget(self, action:#selector(pushVC), for: .touchUpInside)
        
        view.addSubview(userButton)
        userButton.snp.makeConstraints { make in
            make.centerX.equalToSuperview()
            make.centerY.equalTo(centerText.snp.bottom).offset(60)
            make.width.equalTo(220)
            make.height.equalTo(35)
        }
        
        // Org Button
        orgButton.setTitle("An Organization", for: .normal)
        orgButton.titleLabel?.font = UIFont(name: "Roboto-Medium", size: 16)
        orgButton.setTitleColor(UIColor(red: 0.345, green: 0.192, blue: 0.004, alpha: 1), for: .normal)
        orgButton.backgroundColor = UIColor(red: 0.89, green: 0.89, blue: 0.79, alpha: 0.8)
        orgButton.layer.cornerRadius = 10
        orgButton.layer.borderWidth = 1
        orgButton.layer.borderColor = UIColor(red: 0.482, green: 0.529, blue: 0.427, alpha: 0.5).cgColor
        
        orgButton.addTarget(self, action:#selector(pushVC), for: .touchUpInside)
        
        view.addSubview(orgButton)
        orgButton.snp.makeConstraints { make in
            make.centerX.equalToSuperview()
            make.top.equalTo(userButton.snp.bottom).offset(25)
            make.width.equalTo(220)
            make.height.equalTo(35)
        }
    }
    
    @objc private func pushVC(_ VC: UIViewController){
        //let VCtoBePushed = NewAccVC(text: text, delegate: self)
        //navigationController?.pushViewController(VCtoBePushed, animated: true)
    }

}




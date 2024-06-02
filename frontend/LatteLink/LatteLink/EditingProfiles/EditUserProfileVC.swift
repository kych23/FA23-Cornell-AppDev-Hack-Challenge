//
//  EditOrgProfileVC.swift
//  LatteLink
//
//  Created by Kyle Chu on 12/28/23.
//

import UIKit
import SnapKit
import Alamofire

class EditUserProfileVC: UIViewController {
    // MARK: - Properties (Subviews)
    private let scrollView = UIScrollView()
    private let contentView = UIView()
    private let topAccent = UIImageView()
    private let backButton = UIButton()
    private let titleText = UILabel()
    private let pfp = UIButton()
    private let bgp = UIButton()
    private let textUnderPfp = UILabel()
    private var fullNameTextBox = UITextField()
    private var gradYrTextBox = UITextField()
    private var majorTextBox = UITextField()
    private var bioTextBox = UITextView()
    private var orgsCollectionView: UICollectionView!
    
    // MARK: - Properties (Data)
    private var pfpFile = ""
    private var bgpFile = ""
    private var fullName: String = ""
    private var gradYr: Int!
    private var major: String = ""
    private var bio: String = ""
    
    // TODO -> Creating org collection view (do i need to create org objects?)
    private var orgs: [Org] = []
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.navigationItem.hidesBackButton = true
        scrollView.addSubview(contentView)
        view.addSubview(scrollView)
        scrollView.snp.makeConstraints { make in
            make.edges.equalToSuperview()
            make.width.equalTo(scrollView)
        }
        contentView.snp.makeConstraints { make in
            make.edges.equalToSuperview()
            make.width.equalTo(scrollView.snp.width)
        }
        scrollView.layer.backgroundColor = UIColor(red: 1, green: 1, blue: 1, alpha: 1).cgColor
        contentView.layer.backgroundColor = UIColor.yellow.cgColor
        scrollView.isUserInteractionEnabled = true
        contentView.isUserInteractionEnabled = true
        
        setupTopAccent()
        setupBackButton()
        setupTitle()
        setupPhotos()
        setupText()
        setupFullName()
        setupGradYr()
        setupMajor()
        setupBio()
    }
    
    private func setupTopAccent() {
        topAccent.image = UIImage(named: "Accent")
        topAccent.contentMode = .scaleAspectFit
        topAccent.layer.cornerRadius = 10
        
        contentView.addSubview(topAccent)
        topAccent.snp.makeConstraints { make in
            make.top.equalTo(contentView.snp.top).offset(-70)
            make.trailing.equalTo(contentView.snp.trailing)
            make.height.equalTo(230)
            make.width.equalTo(237)
        }
    }
    
    private func setupBackButton() {
        backButton.setImage(UIImage(named: "LeftArrow"), for: .normal)
        backButton.addTarget(self, action:#selector(popVC), for: .touchUpInside)
        backButton.isUserInteractionEnabled = true
        contentView.addSubview(backButton)
        backButton.snp.makeConstraints { make in
            make.leading.equalTo(contentView.snp.leading).offset(40)
            make.top.equalTo(contentView.snp.top)
            make.width.equalTo(26)
            make.height.equalTo(26)
        }
        contentView.bringSubviewToFront(backButton)
    }

    private func setupTitle() {
        titleText.font = UIFont(name: "Roboto-Bold", size: 30)
        titleText.numberOfLines = 0
        titleText.lineBreakMode = .byWordWrapping
        titleText.textColor = UIColor(red: 0.35, green: 0.18, blue: 0.05, alpha: 1)
        titleText.textAlignment = .center
        titleText.text = "Customize Your Profile"
        contentView.addSubview(titleText)
        titleText.snp.makeConstraints { make in
            make.centerX.equalTo(contentView.snp.centerX)
            make.top.equalTo(contentView.snp.top).offset(100)
        }
    }

    private func setupPhotos() {
        // creates and resizes placeholder pfp image
        let pfpPhoto = UIImageView()
        pfpPhoto.image = UIImage(named: "pfpPlaceholder")
        pfpPhoto.contentMode = .scaleAspectFit
        pfpPhoto.frame = CGRect(x: 0, y: 0, width: 38.72, height: 38.72)
        pfpPhoto.snp.makeConstraints { make in
            make.width.height.equalTo(28.72)
        }
        
        // creates the larger square of pfp
        pfp.layer.backgroundColor = UIColor(red: 0.944, green: 0.889, blue: 0.845, alpha: 0.3).cgColor
        pfp.layer.cornerRadius = 8.06
        pfp.addTarget(self, action:#selector(popVC), for: .touchUpInside)
        pfp.setImage(pfpPhoto.image, for: .normal)
        contentView.addSubview(pfp)
        pfp.snp.makeConstraints { make in
            make.leading.equalTo(contentView.snp.leading).offset(83)
            make.top.equalTo(titleText.snp.bottom).offset(18.39)
            make.width.height.equalTo(98)
        }
        contentView.bringSubviewToFront(pfp)
        
        // creates the larger square of background photo (bgp)
        bgp.layer.backgroundColor = UIColor(red: 0.944, green: 0.889, blue: 0.845, alpha: 0.3).cgColor
        bgp.layer.cornerRadius = 8.06
        bgp.addTarget(self, action:#selector(setPicture), for: .touchUpInside)
        contentView.addSubview(bgp)
        bgp.snp.makeConstraints { make in
            make.trailing.equalTo(contentView.snp.trailing).offset(-83)
            make.top.equalTo(titleText.snp.bottom).offset(18.39)
            make.width.height.equalTo(98)
        }
        // adds the inner bgp placeholder
        let bgpPhoto = UIImageView()
        bgp.addSubview(bgpPhoto)
        bgpPhoto.image = UIImage(named: "bgpPlaceholder")
        bgpPhoto.contentMode = .scaleAspectFit
        bgpPhoto.frame = CGRect(x: 0, y: 0, width: 38.72, height: 38.72)
        bgpPhoto.snp.makeConstraints { make in
            make.center.equalTo(bgp.snp.center)
        }
        contentView.bringSubviewToFront(bgp)
    }
    
    // Method to set images from camera roll
    @objc private func setPicture() {
        print("working")
    }
    
    private func setupText() {
        textUnderPfp.font = UIFont(name: "Roboto-Medium", size: 18)
        textUnderPfp.numberOfLines = 0
        textUnderPfp.lineBreakMode = .byWordWrapping
        textUnderPfp.textColor = UIColor(red: 0.345, green: 0.192, blue: 0.004, alpha: 1)
        textUnderPfp.textAlignment = .center
        textUnderPfp.text = "Edit Profile Picture or Background Image"
        
        contentView.addSubview(textUnderPfp)
        
        textUnderPfp.snp.makeConstraints { make in
            make.centerX.equalToSuperview()
            make.top.equalTo(pfp.snp.bottom).offset(19)
        }
    }
    
    private func setupFullName() {
        // sets up the text "Full Name:" next to text field
        let text = UILabel()
        text.font = UIFont(name: "Roboto-Medium", size: 15)
        text.textColor = UIColor(red: 0.345, green: 0.192, blue: 0.004, alpha: 1)
        text.textAlignment = .center
        text.text = "Full Name:"
        contentView.addSubview(text)
        text.snp.makeConstraints { make in
            make.leading.equalTo(contentView.snp.leading).offset(50)
            make.top.equalTo(textUnderPfp.snp.bottom).offset(28.6)
            make.width.equalTo(73)
            make.height.equalTo(17)
        }
        // sets up the text field
        fullNameTextBox = CustomTextField(font: UIFont(name: "Roboto-Medium", size: 14)!, width: 203, height: 30)
        fullNameTextBox.layer.cornerRadius = 8
        fullNameTextBox.layer.borderWidth = 1
        contentView.addSubview(fullNameTextBox)
        fullNameTextBox.snp.makeConstraints { make in
            make.leading.equalTo(text.snp.trailing).offset(17)
            make.centerY.equalTo(text.snp.centerY)
            make.width.equalTo(203.05)
            make.height.equalTo(29.8)
        }
    }
    
    private func setupGradYr() {
        // sets up the text "Grad Year:" next to text field
        let text = UILabel()
        text.font = UIFont(name: "Roboto-Medium", size: 15)
        text.textColor = UIColor(red: 0.345, green: 0.192, blue: 0.004, alpha: 1)
        text.textAlignment = .center
        text.text = "Grad Year:"
        contentView.addSubview(text)
        text.snp.makeConstraints { make in
            make.leading.equalTo(contentView.snp.leading).offset(50)
            make.top.equalTo(fullNameTextBox.snp.bottom).offset(15)
            make.width.equalTo(73)
            make.height.equalTo(17)
        }
        // sets up the text field
        gradYrTextBox = CustomTextField(font: UIFont(name: "Roboto-Medium", size: 14)!, width: 203, height: 30)
        gradYrTextBox.layer.cornerRadius = 8
        gradYrTextBox.layer.borderWidth = 1
        contentView.addSubview(gradYrTextBox)
        gradYrTextBox.snp.makeConstraints { make in
            make.leading.equalTo(text.snp.trailing).offset(17)
            make.centerY.equalTo(text.snp.centerY)
            make.width.equalTo(203.05)
            make.height.equalTo(29.8)
        }
    }
    
    private func setupMajor() {
        // sets up the text "Major/Minor:" next to text field
        let text = UILabel()
        text.font = UIFont(name: "Roboto-Medium", size: 15)
        text.textColor = UIColor(red: 0.345, green: 0.192, blue: 0.004, alpha: 1)
        text.textAlignment = .center
        text.text = "Major/Minor:"
        contentView.addSubview(text)
        text.snp.makeConstraints { make in
            make.trailing.equalTo(gradYrTextBox.snp.leading).offset(-17)
            make.top.equalTo(gradYrTextBox.snp.bottom).offset(15)
            make.width.equalTo(89.5)
            make.height.equalTo(17)
        }
        // sets up the text field
        majorTextBox = CustomTextField(font: UIFont(name: "Roboto-Medium", size: 14)!, width: 203, height: 30)
        majorTextBox.layer.cornerRadius = 8
        majorTextBox.layer.borderWidth = 1
        contentView.addSubview(majorTextBox)
        majorTextBox.snp.makeConstraints { make in
            make.leading.equalTo(text.snp.trailing).offset(17)
            make.centerY.equalTo(text.snp.centerY)
            make.width.equalTo(203.05)
            make.height.equalTo(29.8)
        }
    }
    
    private func setupBio() {
        // sets up the text "Brief Bio:" next to text field
        let text = UILabel()
        text.font = UIFont(name: "Roboto-Medium", size: 15)
        text.textColor = UIColor(red: 0.345, green: 0.192, blue: 0.004, alpha: 1)
        text.textAlignment = .center
        text.text = "Brief Bio:"
        contentView.addSubview(text)
        
        // sets up the text field
        bioTextBox = CustomTextView(font: UIFont(name: "Roboto-Light", size: 12)!, width: 296, height: 107)
        bioTextBox.text = "Just for others to get to know you a bit! Let us know where you’re from, your hobbies, and any other random facts :)"
        bioTextBox.layer.borderWidth = 1.0
        
        contentView.addSubview(bioTextBox)
        bioTextBox.snp.makeConstraints { make in
            make.leading.equalTo(contentView.snp.leading).offset(55.4)
            make.top.equalTo(majorTextBox.snp.bottom).offset(55.4)
            make.width.equalTo(296)
            make.height.equalTo(107)
        }
        // constraints for "Brief Bio:" since it is based on the text field
        text.snp.makeConstraints { make in
            make.leading.equalTo(bioTextBox.snp.leading).offset(-17)
            make.top.equalTo(majorTextBox.snp.centerY).offset(35.5)
            make.width.equalTo(89.5)
            make.height.equalTo(17)
        }
    }
}

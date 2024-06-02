//
//  EditOrgProfileVC.swift
//  LatteLink
//
//  Created by Kyle Chu on 12/28/23.
//

import UIKit
import SnapKit
import Alamofire

class EditOrgProfileVC: UIViewController {
    // MARK: - Properties (Subviews)
    private let scrollView = UIScrollView()
    private let contentView = UIView()
    private let topAccent = UIImageView()
    private let backButton = UIButton()
    private let titleText = UILabel()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        view.addSubview(scrollView)
        scrollView.snp.makeConstraints { make in
            make.top.bottom.trailing.leading.equalToSuperview()
        }
        scrollView.addSubview(contentView)
        contentView.snp.makeConstraints { make in
            make.edges.equalToSuperview()
        }
        view.backgroundColor = UIColor(red: 1, green: 1, blue: 1, alpha: 1)
        contentView.backgroundColor = UIColor(red: 1, green: 1, blue: 1, alpha: 1)

        setupTopAccent()
        setupBackButton()
        setupTitle()
    }
    
    private func setupTopAccent() {
        topAccent.image = UIImage(named: "Accent")
        topAccent.contentMode = .scaleAspectFit
        topAccent.layer.cornerRadius = 10
        contentView.addSubview(topAccent)
        
        topAccent.snp.makeConstraints { make in
            make.top.equalTo(contentView.snp.top).offset(10)
            make.trailing.equalTo(contentView.snp.trailing).offset(20)
            make.height.equalTo(230)
            make.width.equalTo(237)
        }
    }
    
    private func setupBackButton() {
        backButton.setImage(UIImage(named: "LeftArrow"), for: .normal)
        backButton.addTarget(self, action:#selector(popVC), for: .touchUpInside)
        
        view.addSubview(backButton)
        backButton.snp.makeConstraints { make in
            make.leading.equalTo(view.snp.leading).offset(35)
            make.top.equalTo(view.snp.top).offset(89)
            make.width.equalTo(26)
            make.height.equalTo(26)
        }
    }
    
    private func setupTitle() {
        titleText.font = UIFont(name: "Roboto-Bold", size: 28)
        titleText.numberOfLines = 0
        titleText.lineBreakMode = .byWordWrapping
        titleText.textColor = UIColor(red: 0.35, green: 0.18, blue: 0.05, alpha: 1)
        titleText.textAlignment = .center
        titleText.text = "Customize Your Profile"
        contentView.addSubview(titleText)
        titleText.snp.makeConstraints { make in
            make.centerX.equalTo(contentView.snp.centerX)
            make.centerY.equalTo(contentView.snp.centerY).offset(-218)
        }
    }
}

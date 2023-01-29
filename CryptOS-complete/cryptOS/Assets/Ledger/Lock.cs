using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

public class Lock : MonoBehaviour
{
    public Slider Lock_Screen;
    public float lock_timer = 1f;
    public float lock_timer_reset = 1f;

    public void Update()
    {
        if (lock_timer > 0f)
        {
            lock_timer -= Time.deltaTime;
        }

        else if (lock_timer <= 0f)
        {
            if (Lock_Screen.value == 1)
            {
                Lock_Wallet();
            }
            lock_timer = lock_timer_reset;
        }
    }


    public void Lock_Wallet()
    {
        SceneManager.LoadScene("Login");
    }
}
